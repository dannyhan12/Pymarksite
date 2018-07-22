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


@app.route('/pages/<slug>')
def pages(slug):
    app.logger.info('Loading {} page'.format(slug))
    post = Pages.getPageContent('pages/{}.md'.format(slug))
    return render_template(
        'post.html',
        post=post,
        active_page=slug)