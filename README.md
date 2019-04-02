# Pymarksite
Markdown based cms written in Python

# How to install requirements
Run these commands to install required libraries. This will install libraries into a virtual environment.

```
cd web
python3.7 -m venv venv
source venv/bin/activate
python3.7 -m pip install --upgrade pip
python3.7 -m pip install -r requirements.txt
python3.7 db_setup.py
deactivate
```

# How to test
After you install the requirements, run this command.

```
web/venv/bin/python3.7 -m pytest --cov .
```

This should show test results and data on test coverage.

# How to run
After you install the requirements, run this command.

```
export FLASK_APP=web/main
web/venv/bin/python3.7 web/db/db_setup.py
web/venv/bin/python3.7 -m flask run
```

After you run this command, you should be able to open a web browser and view the app at [http://127.0.0.0:5000](http://127.0.0.0:5000]).

# Configuration files
There are a few configuration files to help set up my site.

- `conf/Pymarksite.nginx.conf` - contains details for configuring nginx server
  This can be linked to the nginx conf files `ln -s conf/Pymarksite.nginx.conf /etc/nginx/sites-enabled/Pymarksite.conf`
- `conf/Pymarksite.supervisor.conf` - contains details for configuring supervisor
  This can be linked to the supervisor conf files `ln -s conf/Pymarksite.supervisor.conf /etc/supervisor/conf.d/Pymarksite.conf`
