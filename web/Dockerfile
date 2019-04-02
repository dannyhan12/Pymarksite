FROM python:3.7-alpine

WORKDIR /web

# Copy requirements.txt first, so that we can install components once
# and then re-use the cached image
COPY requirements.txt /web

# Install packages
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt --no-cache-dir

# ADD the rest of the files
ADD . /web

# Set up environment
RUN mkdir -m 777 /var/log/Pymarksite

# Run gunicorn to start the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "/var/log/Pymarksite/app.log", "--error-logfile", "/var/log/Pymarksite/app.log", "--log-level", "info", "--capture-output", "-w", "4", "main:app"]
