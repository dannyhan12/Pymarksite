import os
from markdown import markdown

class PostHeader():
    def __init__(self, title, slug):
        self.title = title
        self.slug = slug

def getPostHeaders(page=0):
    ''' Get information about each post in the content directory.'''
    headers = []
    for f in os.listdir('content'):
        if not f.endswith('.md'): continue

        firstMetaFound = False
        metaData = {}
        with open('content/' + f, 'r') as inputData:
            for line in inputData:
                if not firstMetaFound and line.startswith('-'):
                    firstMetaFound = True
                    continue
                if line.startswith('-'):
                    # End of metadata
                    break
                items = line[:-1].split(':')
                if len(items) > 1:
                    metaData[items[0]] = items[1]
        headers.append(metaData)
    return headers

def getPostContent(slug):
    '''Get the text for a post that matches the specified slug'''
    txt = ''
    for f in os.listdir('content'):
        if not f.endswith('.md'): continue

        firstMetaFound = False
        endMetaFound = False
        slugMatch = False
        with open('content/' + f, 'r') as inputData:
            for line in inputData:
                if not firstMetaFound and line.startswith('-'):
                    firstMetaFound = True
                    continue
                if line.startswith('-'):
                    if slugMatch:
                        endMetaFound = True
                    else:
                        # No matching files, go to next file
                        break
                if endMetaFound:
                    txt += line
                else:
                    items = line[:-1].split(':')
                    if len(items) > 1 and items[0] == "Slug" and items[1] == slug:
                        slugMatch = True

    return markdown(txt)
