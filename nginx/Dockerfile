FROM nginx:latest

RUN rm -rf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/conf.d/sites-available
RUN mkdir -p /etc/nginx/conf.d/sites-enabled

COPY nginx.conf /etc/nginx/nginx.conf
COPY common.conf /etc/nginx/conf.d/common.conf
COPY common_location.conf /etc/nginx/conf.d/common_location.conf
COPY ssl.conf /etc/nginx/conf.d/ssl.conf
COPY cloudloop-nginx.conf /etc/nginx/conf.d/sites-available/cloudloop.conf
RUN ln -s /etc/nginx/conf.d/sites-available/cloudloop.conf /etc/nginx/conf.d/sites-enabled/cloudloop.conf
