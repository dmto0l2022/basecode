# pull official base image
FROM python:3.11.4-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get -y install vim unzip curl netcat gcc && apt-get clean


RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get update && apt-get install -y mariadb-server galera-4 mariadb-client libmariadb3 mariadb-backup mariadb-common
RUN apt-get install -y libmariadb-dev

#WORKDIR /workdir/fastapi_alembic/app

# set working directory
#WORKDIR /usr/src/app

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . ./app
