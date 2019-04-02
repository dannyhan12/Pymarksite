import os
from markdown import Markdown
import sqlite3


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
    query = 'SELECT file_path, title, description FROM headers WHERE slug=?'
    for row in db_cursor.execute(query, (slug,)):
        file_path = row[0]
        title = '# ' + row[1] + '\n'
        description = '**_' + row[2] + '_** \n\n'
        break

    query = 'SELECT tag FROM tags WHERE slug=?'
    db_tags = []
    for row in db_cursor.execute(query, (slug,)):
        db_tags.append(row[0])
    tags = '\n\nTAGS: **_' + ', '.join(db_tags) + '_**  \n'

    content = ''
    try:
        with open(file_path, 'r') as inputData:
            data = inputData.read()
            markers_found = 0  # Wait for 2 markers before reading content
            for line in data.split('\n'):
                if line.startswith('-'):
                    markers_found += 1
                if markers_found < 2:
                    continue
                content += line + '\n'
        content = content.strip()
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
    return MD.convert(title + description + content + tags)
