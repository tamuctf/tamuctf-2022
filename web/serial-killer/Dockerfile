FROM php:7.2-apache
COPY src/ /var/www/html/

RUN chmod +x /var/www/html/start.sh && \
    /var/www/html/start.sh && \
    rm /var/www/html/start.sh