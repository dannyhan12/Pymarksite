import os
from app import app, BlogPosts, Pages
from markdown import markdown
from flask import render_template
import sqlite3


def _get_connection(db_name='pymarksite.db'):
    db_dir = os.path.expanduser(os.environ.get('DB_DIR', '/db'))
    db_path = os.path.join(db_dir, db_name)
    return sqlite3.connect(db_path)


@app.route('/')
@app.route('/index')
@app.route('/writing')
def writing():
    app.logger.info('Loading writing')

    # Get database connection
    cursor = _get_connection().cursor()

    # Get posts and render
    posts = BlogPosts.getPostHeaders(page=0, db_cursor=cursor)
    return render_template('writing.html', posts=posts, active_page='writing')


@app.route('/writing/<slug>')
def post(slug):
    app.logger.info('Loading post {}'.format(slug))

    # Get database connection
    cursor = _get_connection().cursor()

    post = BlogPosts.getPostContent(slug, cursor)
    return render_template(
        'post.html',
        post=post,
        active_page='writing',
        url='https://programmerdays.disqus.com/',
        urlslug=slug,
        title=post.title)


@app.route('/pages/<slug>')
def pages(slug):
    pages_dir = os.path.expanduser(os.environ.get('PAGES_DIR', '/pages'))
    path_of_page = os.path.join(pages_dir, f'{slug}.md')
    app.logger.info(f'Loading from file: {path_of_page}')
    post = Pages.getPageContent(path_of_page)
    return render_template(
        'post.html',
        post=post,
        active_page=slug)
