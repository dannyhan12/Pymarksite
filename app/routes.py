from app import app

from markdown import markdown
from app import BlogPosts
from flask import render_template


@app.route('/')
@app.route('/index')
@app.route('/blog')
def blog():
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('blog.html', posts=posts)


@app.route('/blog/<slug>')
def post(slug):
    post = BlogPosts.getPostContent(slug)
    return render_template('post.html', post=post)


@app.route('/projects')
@app.route('/about')
def wip():
    return render_template('post.html', post="Work in progress ...")

