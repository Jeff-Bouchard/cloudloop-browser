FROM nginx:latest

RUN apt-get update && apt-get install -y libcap2-bin

RUN rm -rf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/conf.d/sites-available
RUN mkdir -p /etc/nginx/conf.d/sites-enabled

RUN setcap 'cap_net_bind_service=+eip' /usr/sbin/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY common.conf /etc/nginx/common.conf
COPY common_location.conf /etc/nginx/common_location.conf
COPY ssl.conf /etc/nginx/ssl.conf
COPY cloudloop-nginx.conf /etc/nginx/conf.d/sites-available/cloudloop.conf
RUN ln -s /etc/nginx/conf.d/sites-available/cloudloop.conf /etc/nginx/conf.d/sites-enabled/cloudloop.conf
