import os
from markdown import Markdown
import sqlite3


def _get_prev_next(db_cursor, post_date):
    # Get links for next post
    query = '''SELECT slug, title FROM headers 
                WHERE post_date > ?
                ORDER BY post_date
                LIMIT 1'''
    next_link = ''
    for row in db_cursor.execute(query, (post_date,)):
        next_slug = row[0]
        next_title = row[1]
        next_link = f'Next: [{next_title}]({next_slug})'

    # Get links for previous post
    query = '''SELECT slug, title FROM headers 
                WHERE post_date < ?
                ORDER BY post_date desc
                LIMIT 1'''
    prev_link = ''
    for row in db_cursor.execute(query, (post_date,)):
        prev_slug = row[0]
        prev_title = row[1]
        prev_link = f'Previous: [{prev_title}]({prev_slug})'

    # Create text for previous and next links
    next_prev = (f'{prev_link}\n\n' if len(prev_link) > 0 else '') + \
                (f'{next_link}' if len(next_link) > 0 else '')

    # Return text
    return f'\n{next_prev}\n' if len(next_prev) > 0 else ''


def getPostHeaders(page=0, db_cursor=None):
    ''' Get information about each post in the content directory.'''
    query = 'SELECT slug, title, post_date FROM headers ORDER BY post_date desc'
    headers = []
    for row in db_cursor.execute(query):
        headers.append({
            'Slug': row[0],
            'Title': row[1],
            'Date': row[2]
        })
    headers.sort(key=lambda x: x['Date'], reverse=True)
    return headers


def getPostContent(slug, db_cursor):
    '''Get the text for a post that matches the specified slug'''
    query = 'SELECT file_path, title, description, post_date FROM headers WHERE slug=?'
    for row in db_cursor.execute(query, (slug,)):
        file_path = row[0]
        title = '# ' + row[1] + '  \n\n'
        description = '**_' + row[2] + '_**  \n'
        post_date = row[3]
        break

    query = 'SELECT tag FROM tags WHERE slug=?'
    db_tags = []
    for row in db_cursor.execute(query, (slug,)):
        db_tags.append(row[0])
    tags = f'\nTAGS: **_ {", ".join(db_tags)} _**  \n'

    # Create text for previous and next links
    next_prev = _get_prev_next(db_cursor, post_date)

    content = ''
    try:
        with open(file_path, 'r') as inputData:
            data = inputData.read()
            markers_found = 0  # Wait for 2 markers before reading content
            for line in data.split('\n'):
                if markers_found < 2:
                    if line.startswith('-'):
                        markers_found += 1
                else:
                    content += line + '\n'
        content = content.strip() + '\n'
    except FileNotFoundError as e:
        content += f'Cannot find file: {file_path}'

    MD = Markdown(
        extensions=[
            "markdown.extensions.codehilite",
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
        ]
    )
    return MD.convert(title + description + tags + content + next_prev)
