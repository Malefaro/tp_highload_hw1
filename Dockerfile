FROM python:slim

MAINTAINER Grigoryev Pavel

COPY ./ /custom_server

RUN pip install -r ./custom_server/requirements.txt

EXPOSE 80

WORKDIR /custom_server

USER root

CMD python3.6 ./main.py