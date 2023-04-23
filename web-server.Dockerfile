FROM nginx

WORKDIR /etc/nginx

COPY default.conf /etc/nginx/conf.d

EXPOSE 8080
