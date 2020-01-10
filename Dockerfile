FROM python:3.6
MAINTAINER Holker Dev

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN apt-get update
RUN apt-get -y install software-properties-common
RUN apt-get -y install gfortran python-dev libopenblas-dev liblapack-dev cython
RUN apt-get -y install postgresql-client libjpeg-dev
RUN apt-get -y install gcc libc-dev postgresql-server-dev-11 musl-dev zlib1g-dev

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser --disabled-password user

RUN chown -R user:user /vol/
RUN chown -R 755 /vol/web

USER user