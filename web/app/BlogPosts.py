import os
from markdown import Markdown
BLOG_POSTS_DIR = '/content/posts'

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
    for f in os.listdir(BLOG_POSTS_DIR):
        if not f.endswith('.md'):
            continue

        firstMetaFound = False
        metaData = {}
        with open(os.path.join(BLOG_POSTS_DIR, f), 'r') as inputData:
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
    for f in os.listdir(BLOG_POSTS_DIR):
        if not f.endswith('.md'):
            continue

        firstMetaFound = False
        endMetaFound = False
        slugMatch = False
        with open(os.path.join(BLOG_POSTS_DIR, f), 'r') as inputData:
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
                    txt += line
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
