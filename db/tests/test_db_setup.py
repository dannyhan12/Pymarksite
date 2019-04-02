from db_setup import add_data, create_tables, get_connection, _DB_PATH
import os
import pytest
import sqlite3
from unittest.mock import mock_open, patch

TEST_DB_NAME = 'test.db'
TEST_DB_PATH = os.path.join(_DB_PATH, TEST_DB_NAME)
TEST_POST_DATA = '---\n' + \
    'Title: A sample title\n' + \
    'Description: A sample description\n' + \
    'Tags: SAMPLE, tAg\n' + \
    'Slug: a-sample-slug\n' + \
    'Date: 1999/01/31\n' + \
    '---\n' + \
    'test post content'


@pytest.fixture
def _setup_and_teardown():
    def _remove():
        try:
            os.remove(TEST_DB_PATH)
        except FileNotFoundError:
            pass

    # Return a callable - to clean up the database before we start
    yield _remove

    # When the test is over, clean up the database again
    _remove()


def test_db_setup_smoke_test(_setup_and_teardown):
   # GIVEN: No database
    _setup_and_teardown()

    # WHEN: Database is created
    create_tables(get_connection('test.db'))

    # THEN: We should be able to make a SELECT query
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM headers''')


def test_db_setup_multiple_create_is_safe(_setup_and_teardown):
   # GIVEN: No database
    _setup_and_teardown()

    # WHEN: Database is called multiple times
    # THEN: there should be no problems
    db_conn = get_connection('test.db')
    create_tables(db_conn)
    create_tables(db_conn)
    create_tables(db_conn)
    create_tables(db_conn)


@patch("os.path.getmtime")
@patch("os.listdir")
def test_add_data_update_headers(mock_list_dir, mock_getmtime, _setup_and_teardown):
    db_conn = get_connection('test.db')
    create_tables(db_conn)

    with patch('db.db_setup.open', mock_open(read_data=TEST_POST_DATA)):
        mock_list_dir.return_value = ['one-file.md']
        mock_getmtime.return_value = 12345.789
        add_data(db_conn, 'test_dir')

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT slug,
        file_path,
        file_mtime,
        title,
        post_date,
        description 
        FROM headers''').fetchall()

    assert len(rows) == 1
    assert rows[0][0] == 'a-sample-slug'
    assert os.path.basename(rows[0][1]) == 'one-file.md'
    assert rows[0][2] == 12345
    assert rows[0][3] == 'A sample title'
    assert rows[0][4] == '1999/01/31'
    assert rows[0][5] == 'A sample description'


@patch("os.path.getmtime")
@patch("os.listdir")
def test_add_data_update_tags(mock_list_dir, mock_getmtime, _setup_and_teardown):
    db_conn = get_connection('test.db')
    create_tables(db_conn)

    with patch('db.db_setup.open', mock_open(read_data=TEST_POST_DATA)):
        mock_list_dir.return_value = ['one-file.md']
        add_data(db_conn, 'test_dir')

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    rows = cursor.execute('SELECT slug, tag FROM tags ORDER BY tag').fetchall()

    assert len(rows) == 2
    assert rows[0][0] == 'a-sample-slug'
    assert rows[0][1] == 'sample'
    assert rows[1][0] == 'a-sample-slug'
    assert rows[1][1] == 'tag'


@patch("os.path.getmtime")
@patch("os.listdir")
def test_record_update(mock_list_dir, mock_getmtime, _setup_and_teardown):
    print('in test_add_data_smoke_test')
    db_conn = get_connection('test.db')
    create_tables(db_conn)

    with patch('db.db_setup.open', mock_open(read_data=TEST_POST_DATA)):
        mock_list_dir.return_value = ['one-file.md']
        mock_getmtime.return_value = 1
        add_data(db_conn, 'test_dir')

    updated_data = TEST_POST_DATA.replace('A sample title', 'a new title')
    with patch('db.db_setup.open', mock_open(read_data=updated_data)):
        mock_list_dir.return_value = ['one-file.md']
        mock_getmtime.return_value = 2
        add_data(db_conn, 'test_dir')

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT title FROM headers''').fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 'a new title'


@patch("os.path.getmtime")
@patch("os.listdir")
def test_record_unchanged_record(mock_list_dir, mock_getmtime, _setup_and_teardown):
    print('in test_add_data_smoke_test')
    db_conn = get_connection('test.db')
    create_tables(db_conn)

    with patch('db.db_setup.open', mock_open(read_data=TEST_POST_DATA)):
        mock_list_dir.return_value = ['one-file.md']
        mock_getmtime.return_value = 1
        add_data(db_conn, 'test_dir')

    updated_data = TEST_POST_DATA.replace('A sample title', 'a new title')
    with patch('db.db_setup.open', mock_open(read_data=updated_data)):
        mock_list_dir.return_value = ['one-file.md']
        mock_getmtime.return_value = 1
        add_data(db_conn, 'test_dir')

    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT title FROM headers''').fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 'A sample title'
