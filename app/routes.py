from app import app

from markdown import markdown
from app import BlogPosts
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('blog.html', posts=posts, active_page='index')

@app.route('/blog')
def blog():
    posts = BlogPosts.getPostHeaders(page=0)
    return render_template('blog.html', posts=posts, active_page='blog')

@app.route('/blog/<slug>')
def post(slug):
    post = BlogPosts.getPostContent(slug)
    return render_template('post.html', post=post, active_page='blog')

@app.route('/projects')
def projects():
    return render_template('post.html', post="Work in progress ...", active_page='projects')


@app.route('/about')
def about():
    return render_template('post.html', post="Work in progress ...", active_page='about')
