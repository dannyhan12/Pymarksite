import os
from app import app
from markdown import markdown
from app import BlogPosts
from app import Pages
from flask import render_template


@app.route('/')
@app.route('/index')
@app.route('/writing')
def writing():
    app.logger.info('Loading writing')
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('writing.html', posts=posts, active_page='writing')


@app.route('/writing/<slug>')
def post(slug):
    app.logger.info('Loading post {}'.format(slug))
    post = BlogPosts.getPostContent(slug)
    return render_template(
        'post.html',
        post=post,
        active_page='writing',
        url='https://programmerdays.disqus.com/',
        urlslug=slug,
        title=post.title)


@app.route('/pages/<slug>')
def pages(slug):
    PAGES_DIR = '/content/pages'
    app.logger.info('Loading {} page'.format(slug))
    post = Pages.getPageContent(os.path.join(PAGES_DIR, '{}.md'.format(slug)))
    return render_template(
        'post.html',
        post=post,
        active_page=slug)
