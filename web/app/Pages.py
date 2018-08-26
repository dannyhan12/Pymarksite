from markdown import Markdown


def getPageContent(pathToPage):
    '''Get the text for a page that matches the specified slug'''
    txt = ''
    with open(pathToPage, 'r') as inputData:
        txt = inputData.read()

    MD = Markdown(
        extensions=[
            "markdown.extensions.codehilite",
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
        ]
    )

    return MD.convert(txt)
