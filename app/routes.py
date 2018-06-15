from app import app

from markdown import markdown
from app import BlogPosts
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    app.logger.info('Loading index')
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('blog.html', posts=posts, active_page='index')


@app.route('/blog')
def blog():
    app.logger.info('Loading blog')
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('blog.html', posts=posts, active_page='blog')


@app.route('/blog/<slug>')
def post(slug):
    app.logger.info('Loading post {}'.format(slug))
    post = BlogPosts.getPostContent(slug)
    return render_template(
        'post.html',
        post=post,
        active_page='blog',
        url='https://programmerdays.disqus.com/',
        urlslug=slug,
        title=post.title)


@app.route('/projects')
def projects():
    app.logger.info('Loading projects')
    return render_template(
        'post.html',
        post="Work in progress ...",
        active_page='projects')


@app.route('/about')
def about():
    app.logger.info('Loading about')
    return render_template(
        'post.html',
        post="Work in progress ...",
        active_page='about')
