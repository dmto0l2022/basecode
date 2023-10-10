# pull official base image
FROM python:3.11.4-bullseye


ARG BUILD_ENV_USERNAME
ARG BUILD_ENV_UID
ARG BUILD_ENV_GID 
ARG BUILD_ENV_GROUPNAME

###

ENV ENV_USERNAME=$BUILD_ENV_USERNAME
ENV ENV_USER_UID=$BUILD_ENV_UID
ENV ENV_USER_GID=$BUILD_ENV_GID 
ENV ENV_USER_GROUPNAME=$BUILD_ENV_GROUPNAME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get -y install vim unzip curl netcat gcc && apt-get clean

RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get update && apt-get install -y mariadb-server galera-4 mariadb-client libmariadb3 mariadb-backup mariadb-common
RUN apt-get install -y libmariadb-dev

WORKDIR /workdir/fastapi_about/app

RUN echo groupadd --gid ${ENV_USER_GID} ${ENV_USER_GROUPNAME}
RUN groupadd --gid ${ENV_USER_GID} ${ENV_USER_GROUPNAME}
RUN echo useradd --uid ${ENV_USER_UID} --gid ${ENV_USER_GID} -m ${ENV_USERNAME}
RUN useradd --uid ${ENV_USER_UID} --gid ${ENV_USER_GID} -m ${ENV_USERNAME}

RUN chown -R ${ENV_USER_UID}:${ENV_USER_GID} /workdir

RUN mkdir /env
RUN chown ${ENV_USER_UID}:${ENV_USER_GID} /env
RUN chmod g+s /env

USER ${ENV_USERNAME}

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

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8016", "--reload"]
