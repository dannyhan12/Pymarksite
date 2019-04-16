import os
from app import app, BlogPosts, Pages
from markdown import markdown
from flask import render_template
import sqlite3

DB_PATH = os.environ.get('DB_PATH', '/db')


def get_connection(db_name='pymarksite.db'):
    db_path = os.path.join(DB_PATH, db_name)
    return sqlite3.connect(db_path)


@app.route('/')
@app.route('/index')
@app.route('/writing')
def writing():
    app.logger.info('Loading writing')

    # Get database connection
    cursor = get_connection().cursor()

    # Get posts and render
    posts = BlogPosts.getPostHeaders(page=0, db_cursor=cursor)
    return render_template('writing.html', posts=posts, active_page='writing')


@app.route('/writing/<slug>')
def post(slug):
    app.logger.info('Loading post {}'.format(slug))

    # Get database connection
    cursor = get_connection().cursor()

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
    PAGES_DIR = '/pages'
    app.logger.info('Loading {} page'.format(slug))
    post = Pages.getPageContent(os.path.join(PAGES_DIR, '{}.md'.format(slug)))
    return render_template(
        'post.html',
        post=post,
        active_page=slug)
