from app import app

from markdown import markdown
from app import BlogPosts
from app import Pages
from flask import render_template


@app.route('/')
@app.route('/index')
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
    app.logger.info('Loading projects page')
    post = Pages.getPageContent('pages/projects.md')
    return render_template(
        'post.html',
        post=post,
        active_page='projects')


@app.route('/about')
def about():
    app.logger.info('Loading about page')
    post = Pages.getPageContent('pages/about.md')
    return render_template(
        'post.html',
        post=post,
        active_page='about')
