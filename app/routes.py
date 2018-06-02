from app import app
from markdown import markdown
from app import BlogPosts

@app.route('/')
@app.route('/index')
@app.route('/blog')
def blog():
    md =  "# Welcome\n"
    md += " {I am a programmer: this is how I spend my days}\n\n"
    md += "# Blog posts\n"
    posts = BlogPosts.getPostHeaders(page=0)

    for p in posts:
        md += f'[{p["Title"]}](blog/{p["Slug"]})'
    return markdown(md)

@app.route('/blog/<slug>')
def post(slug):

    post = BlogPosts.getPostContent(slug)
    
    return post
