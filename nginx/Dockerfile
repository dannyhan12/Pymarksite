FROM nginx:alpine

# Remove default configuration which tries to set up connection to port 80
RUN rm /etc/nginx/conf.d/default.conf

# Add directory for logging
RUN mkdir -m 777 /var/log/Pymarksite

# Add configuration file
COPY nginx.conf /etc/nginx/conf.d/pymarksite.nginx.conf
