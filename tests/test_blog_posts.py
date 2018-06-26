from app.BlogPosts import getPostHeaders
from unittest.mock import mock_open, patch


def test_get_post_content():
    assert 1 == 1


@patch("os.listdir")
def test_get_blank_file_returns_no_headers(mockListDir):

    blank_file_txt = ''
    with patch('app.BlogPosts.open', mock_open(read_data=blank_file_txt)):
        mockListDir.return_value = ['one-file.md', 'one-file-to-skip']
        headers = getPostHeaders()
        assert len(headers) == 0


@patch("os.listdir")
def test_get_1_valid_file_returns_1_header(mockListDir):

    sample_meta_data = '---\n' + \
        'Title: A sample title\n' + \
        'Slug: a-sample-slug\n' + \
        'Date: 1999/01/31\n' + \
        '---'
    with patch('app.BlogPosts.open', mock_open(read_data=sample_meta_data)):
        mockListDir.return_value = ['one-file.md']
        headers = getPostHeaders()
        assert len(headers) == 1

        assert headers[0]['Title'] == 'A sample title'
