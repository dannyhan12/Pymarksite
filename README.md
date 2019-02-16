# Pymarksite
Markdown based cms written in Python

# How to install requirements
Run these commands to install required libraries. This will install libraries into a virtual environment.

```
cd web
python3.6 -m venv venv
source venv/bin/activate
python3.6 -m pip install --upgrade pip
python3.6 -m pip install -r requirements.txt
deactivate
```

# How to test
After you install the requirements, run these commands.

```
source web/venv/bin/activate
python3.6 -m pytest --cov .
deactivate
```

This should show test results and data on test coverage.

# How to run
After you install the requirements, run these commands.

```
source web/venv/bin/activate
export FLASK_DEBUG=1
flask run
deactivate
```

After you run the last command, you should be able to open a web browser and view the app at [http://127.0.0.0:5000](http://127.0.0.0:5000]).

# Configuration files
There are a few configuration files to help set up my site.

- `conf/Pymarksite.nginx.conf` - contains details for configuring nginx server
  This can be linked to the nginx conf files `ln -s conf/Pymarksite.nginx.conf /etc/nginx/sites-enabled/Pymarksite.conf`
- `conf/Pymarksite.supervisor.conf` - contains details for configuring supervisor
  This can be linked to the supervisor conf files `ln -s conf/Pymarksite.supervisor.conf /etc/supervisor/conf.d/Pymarksite.conf`
