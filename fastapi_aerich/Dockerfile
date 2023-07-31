
#FROM python:3.10.9-slim-bullseye
##3.10.9-slim-bullseye, 3.10-slim-bullseye, 3.10.9-slim, 3.10-slim
#FROM python:3.10.9-slim-bullseye
FROM python:3.11.4-bullseye
RUN apt-get update && apt-get -y install vim netcat gcc unzip && apt-get clean


RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get install -y mariadb-server galera-4 mariadb-client libmariadb3 mariadb-backup mariadb-common

RUN apt-get install -y libmariadb-dev

WORKDIR /app
COPY app/ /app/
RUN ls -la /app/*

RUN mkdir /env

ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN /env/bin/python3 -m pip install --upgrade pip
RUN . /env/bin/activate
RUN /env/bin/python3 --version
RUN whereis python3
RUN whereis pip3

COPY ./requirements.txt /env/requirements.txt
RUN /env/bin/pip3 install -r /env/requirements.txt
RUN /env/bin/pip3 freeze

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012"]


