from app import app
from markdown import markdown

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/blog')
def blog():
    md = "# Blog posts\n"

    # Todo get posts and slugs from blog directory
    md += "[Setting up a secure web application]"
    md += "(/blog/setting-up-a-secure-web-application)"
    return markdown(md)

@app.route('/blog/<slug>')
def post(slug):
    try:
        with open(f'blog/{slug}.md') as input:
            return markdown(input.read)
    except IOError:
        return f'Cannot find post: "{slug}"'
