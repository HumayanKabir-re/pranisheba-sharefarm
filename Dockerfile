FROM python:3.8.5-slim-buster
#FROM python:3.7-buster
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
WORKDIR /aps_shared_farm

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /aps_shared_farm/
RUN pip3 install -r /aps_shared_farm/requirements.txt

COPY . /aps_shared_farm
RUN ./manage.py collectstatic --no-input
