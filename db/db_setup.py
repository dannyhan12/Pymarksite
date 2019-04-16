'''Script to set up database tables and data.'''
import os
import sqlite3
import sys


def _isValidHeader(header):
    '''Return true if the header contains the minimum set of valid fields.'''
    keys = ['Title', 'Slug', 'Date']
    for k in keys:
        if k not in header or not header[k]:
            return False
    return True


def _get_post_headers(posts_dir):
    ''' Get information about each post in the content directory.'''
    headers = []
    for f in os.listdir(posts_dir):
        if not f.endswith('.md'):
            continue

        file_path = os.path.realpath(os.path.join(posts_dir, f))
        modification_time = int(os.path.getmtime(file_path))

        firstMetaFound = False
        metaData = {
            'mtime': modification_time,
            'file_path': file_path
        }
        with open(file_path, 'r') as inputData:
            data = inputData.read()
            for rawLine in data.split('\n'):
                line = rawLine.strip()
                if not firstMetaFound and line.startswith('-'):
                    firstMetaFound = True
                    continue
                if line.startswith('-'):
                    # End of metadata
                    break
                items = line.split(':')
                if len(items) > 1:
                    metaData[items[0].strip()] = items[1].strip()
        if _isValidHeader(metaData):
            headers.append(metaData)

    headers.sort(key=lambda x: x['Date'], reverse=True)
    return headers


def create_tables(db_conn):
    """Create tables"""
    cursor = db_conn.cursor()

    # Add table
    cursor.execute('''CREATE TABLE IF NOT EXISTS headers (
        slug TEXT PRIMARY KEY,
        file_path TEXT,
        file_mtime INTEGER,
        title TEXT,
        post_date TEXT,
        description TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tags (
        slug text,
        tag text
    )''')

    # Add keys and indices
    # try:
    #    cursor.execute('''CREATE INDEX update_datetime_idx
    #        ON headers(update_datetime DESC)''')
    # except sqlite3.OperationalError:
    #    cursor.execute('''DROP INDEX update_datetime_idx''')
    #    cursor.execute('''CREATE INDEX update_datetime_idx
    #        ON headers(update_datetime DESC)''')
    db_conn.commit()


def drop_tables(db_conn):
    """Remove tables"""
    cursor = db_conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS headers''')
    cursor.execute('''DROP TABLE IF EXISTS tags''')
    db_conn.commit()


def add_data(db_conn, posts_dir):
    # TODO add select in db to get last update time
    # TODO only get headers older than the last update time
    cursor = db_conn.cursor()

    headers = _get_post_headers(posts_dir)
    for h in headers:
        try:
            # Try to insert into table
            query = '''INSERT INTO headers
                (slug, file_path, file_mtime, title, post_date, description)
                VALUES(?, ?, ?, ?, ?, ?)'''
            values = (h['Slug'], h['file_path'], h['mtime'],
                      h['Title'], h['Date'], h['Description'])
            cursor.execute(query, values)
        except sqlite3.IntegrityError:
            # Update the table
            query = '''UPDATE headers
                    SET file_mtime=?, title=?, post_date=?
                    WHERE slug=? AND file_mtime < ?
                '''
            values = (h['mtime'], h['Title'], h['Date'], h['Slug'], h['mtime'])
            cursor.execute(query, values)

        for t in h['Tags'].split(','):
            tag = t.strip().lower()
            if len(tag) == 0:
                continue
            try:
                # Try to insert into table
                cursor.execute('''INSERT INTO tags (slug, tag) VALUES(?, ?)''',
                               (h['Slug'], tag))
            except sqlite3.IntegrityError:
                pass

    db_conn.commit()


def get_connection(db_dir, db_name='pymarksite.db'):
    os.makedirs(db_dir, exist_ok=True)

    db_path = os.path.join(db_dir, db_name)
    return sqlite3.connect(db_path)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        raise RuntimeError('Need 2 arguments. db_setup.py'
                           ' <blog_posts_input_dir> <database_output_dir>')

    posts_dir = sys.argv[1]
    database_dir = sys.argv[2]

    db_conn = get_connection(database_dir, db_name='pymarksite.db')

    drop_tables(db_conn)

    create_tables(db_conn)

    add_data(db_conn, posts_dir)
