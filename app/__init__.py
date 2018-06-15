from flask import Flask
from flask_bootstrap import Bootstrap
from os import environ
import logging

# Create app
app = Flask(__name__)
from app import routes
bootstrap = Bootstrap(app)

# Set up logging
if not environ.get('FLASK_DEBUG', False):
    # Add logging for gunicorn server app
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Add heart beat log
app.logger.info('Hello World. App is ready to serve you now!')
