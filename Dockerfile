FROM python:slim

MAINTAINER Grigoryev Pavel

ADD ./ /custom_server
ADD ./tests/httptest /var/www/html/httptest/
ADD ./httpd.conf /etc/

RUN pip install -r ./custom_server/requirements.txt

EXPOSE 80

WORKDIR /custom_server

USER root

CMD [ "python3.6", "./main.py" ]