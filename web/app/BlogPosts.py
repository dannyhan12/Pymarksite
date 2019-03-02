import os
from markdown import Markdown
_BLOG_POSTS_DIR = None


def _blog_posts_dir():
    '''Get the directory where blog post files exist

    return (str):
        path of blog post directory
    '''
    global _BLOG_POSTS_DIR
    if _BLOG_POSTS_DIR:
        return _BLOG_POSTS_DIR

    if os.path.exists('/content/posts'):
        _BLOG_POSTS_DIR = '/content/posts'
        return _BLOG_POSTS_DIR

    current_dir = os.path.dirname(os.path.abspath(__file__))
    _BLOG_POSTS_DIR = os.path.join(current_dir, '../../content/posts')
    return _BLOG_POSTS_DIR


def _isValidHeader(header):
    '''Return true if the header contains the minimum set of valid fields.'''
    keys = ['Title', 'Slug', 'Date']
    for k in keys:
        if k not in header or not header[k]:
            return False
    return True


def getPostHeaders(page=0):
    ''' Get information about each post in the content directory.'''
    headers = []
    for f in os.listdir(_blog_posts_dir()):
        if not f.endswith('.md'):
            continue

        firstMetaFound = False
        metaData = {}
        with open(os.path.join(_blog_posts_dir(), f), 'r') as inputData:
            data = inputData.read()
            for rawLine in data.split('\n'):
                line = rawLine.strip()
                if not firstMetaFound and line.startswith('-'):
                    firstMetaFound = True
                    continue
                if line.startswith('-'):
                    # End of metadata
                    break
                items = line.split(':')
                if len(items) > 1:
                    metaData[items[0].strip()] = items[1].strip()
        if _isValidHeader(metaData):
            headers.append(metaData)

    headers.sort(key=lambda x: x['Date'], reverse=True)
    return headers


def getPostContent(slug):
    '''Get the text for a post that matches the specified slug'''
    txt = ''
    for f in os.listdir(_blog_posts_dir()):
        if not f.endswith('.md'):
            continue

        firstMetaFound = False
        endMetaFound = False
        slugMatch = False
        with open(os.path.join(_blog_posts_dir(), f), 'r') as inputData:
            data = inputData.read()
            for line in data.split('\n'):
                if not firstMetaFound and line.startswith('-'):
                    firstMetaFound = True
                    continue
                if line.startswith('-'):
                    if slugMatch:
                        endMetaFound = True
                        continue
                    else:
                        # No matching files, go to next file
                        break
                if endMetaFound:
                    txt += line + '\n'
                else:
                    items = line.split(':')
                    if len(items) > 1 and items[0].strip() == "Slug" and \
                            items[1].strip() == slug:
                        slugMatch = True

    MD = Markdown(
        extensions=[
            "markdown.extensions.codehilite",
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
        ]
    )

    return MD.convert(txt)
