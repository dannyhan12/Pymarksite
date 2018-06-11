# Pymarksite
Markdown based cms written in Python

# How to run (on a test machine)
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_DEBUG=1
flask run
```

# Configuration files
There are a few configuration files to help set up my site.

- `conf/Pymarksite.nginx.conf` - contains details for configuring nginx server
  This can be linked to the nginx conf files `ln -s conf/Pymarksite.nginx.conf /etc/nginx/sites-enabled/Pymarksite.conf`
- `conf/Pymarksite.supervisor.conf` - contains details for configuring supervisor
  This can be linked to the supervisor conf files `ln -s conf/Pymarksite.supervisor.conf /etc/supervisor/conf.d/Pymarksite.conf`
