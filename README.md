# Pymarksite
Markdown based cms (content management system, aka blog) written in Python

This project can be used to host a web site. I use this project to host my site. Of course, your mileage may vary.

# How to install and run with Docker

The following instructions can be used to run this application in docker. This sets up a database, starts up the web application and starts an nginx web server. If it works, this is the easiest way to get up and running.

```
docker-compose down;
docker-compose build;
docker-compose up;
```

After the docker images are up, you can test the server at either port 8000 or 8080. [http://127.0.0.1:8000](http://127.0.0.1:8000) will send requests to gunicorn, while [http://127.0.0.1:8080](http://127.0.0.1:8080) will send requests through nginx to gunicorn.


# Install and run in a virtual environment

The following instructions can be used to install, develop and test in a python virtual environment.

## Install requirements in a virtual environment

```
python3.7 -m venv web/venv
source web/venv/bin/activate
python3.7 -m pip install --upgrade pip
python3.7 -m pip install -r web/requirements.txt
deactivate
```

## Test code in virtual environment
After you install the requirements, run this command.

```
source web/venv/bin/activate
web/venv/bin/python3.7 -m pytest --cov .
```

This should show test results and data on test coverage.

## Set up the database in virtual environment
```
source web/venv/bin/activate
web/venv/bin/python3.7 db/db_setup.py contents/posts db
```

This should create a file called `db/pymarksite.db`, which is a sqlite database file. It contains data about your blog posts.

## Run server in virtual environment
After you install the requirements, run this command.

```
export FLASK_APP=web/main
web/venv/bin/python3.7 -m flask run
```

After you run this command, you should be able to open a web browser and view the app at [http://127.0.0.1:5000](http://127.0.0.1:5000]).
