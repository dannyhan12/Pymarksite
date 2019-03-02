from app.BlogPosts import getPostHeaders, getPostContent
from unittest.mock import mock_open, patch

SAMPLE_POST_DATA = '---\n' + \
    'Title: A sample title\n' + \
    'Description: A sample description\n' + \
    'Tags: sample, tag\n' + \
    'Slug: a-sample-slug\n' + \
    'Date: 1999/01/31\n' + \
    '---\n' + \
    'test post content'


@patch("os.listdir")
def test_get_blank_file_returns_no_headers(mockListDir):

    blank_file_txt = ''
    with patch('app.BlogPosts.open', mock_open(read_data=blank_file_txt)):
        mockListDir.return_value = ['one-file.md', 'one-file-to-skip']
        headers = getPostHeaders()
        assert len(headers) == 0


@patch("os.listdir")
def test_get_1_valid_file_returns_1_header(mockListDir):

    with patch('app.BlogPosts.open', mock_open(read_data=SAMPLE_POST_DATA)):
        mockListDir.return_value = ['one-file.md']
        headers = getPostHeaders()
        assert len(headers) == 1

        assert headers[0]['Title'] == 'A sample title'


@patch("os.listdir")
def test_get_article_by_slug_works(mockListDir):

    with patch('app.BlogPosts.open', mock_open(read_data=SAMPLE_POST_DATA)):
        mockListDir.return_value = ['one-file.md']
        content = getPostContent('a-sample-slug')
        assert 'test post content' in content
        assert 'A sample title' in content
        assert 'A sample description' in content
        assert 'A sample description' in content
        assert 'SAMPLE, TAG' in content
