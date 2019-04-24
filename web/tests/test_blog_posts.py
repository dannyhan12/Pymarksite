import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

from app.BlogPosts import getPostHeaders, getPostContent
from unittest.mock import mock_open, patch, MagicMock

SAMPLE_POST_DATA = '---\n' + \
    'some_meta_data_key: some-meta-data-stuff\n' + \
    '---\n' + \
    'test post content'


@patch("os.listdir")
def test_get_1_valid_file_returns_1_header(mockListDir):
    db_cursor = MagicMock()
    db_cursor.execute.return_value = [['abc', 'A sample title', 'def']]
    mockListDir.return_value = ['one-file.md']
    headers = getPostHeaders(db_cursor=db_cursor)
    assert len(headers) == 1
    assert headers[0]['Title'] == 'A sample title'


@patch("os.listdir")
def test_get_article_by_slug_works(mockListDir):
    db_cursor = MagicMock()
    db_cursor.execute.side_effect = [
        [['some-file-path', 'A sample title', 'A sample description']],
        [['SAMPLE'], ['TAG1234']]
    ]
    with patch('app.BlogPosts.open', mock_open(read_data=SAMPLE_POST_DATA)):
        mockListDir.return_value = ['some-file-path']
        content = getPostContent('a-sample-slug', db_cursor)
        print(content)
        assert 'test post content' in content
        assert 'A sample title' in content
        assert 'A sample description' in content
        assert 'SAMPLE, TAG1234' in content
