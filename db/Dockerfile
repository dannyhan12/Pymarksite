FROM python:3.7-alpine

WORKDIR /db

ADD . /db

ENTRYPOINT ["python3.7", "/db/db_setup.py", "/content/test_posts", "/db"]
