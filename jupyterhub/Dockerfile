FROM python:3

#FROM ubuntu:latest
RUN apt-get update && apt-get -y update \
    && apt-get -y install openssl \
    && apt-get -y install sudo \
    && apt-get install -y apt-utils dialog \
    && apt-get install -y build-essential python3.10 python3-pip python3-dev \
    && apt-get -y install nodejs npm

RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

## helps setup rootless docker
RUN apt-get install -y uidmap
# Load ip_tables module
##RUN /usr/sbin/modprobe ip_tables
RUN apt-get install iptables


RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get update && apt-get install -y mariadb-server galera-4 mariadb-client libmariadb3 mariadb-backup mariadb-common
RUN apt-get install libmariadb-dev

RUN npm install -g configurable-http-proxy

RUN mkdir /workdir
RUN groupadd project


#RUN mkdir /workdir
#RUN chmod -R 2775 /workdir
RUN mkdir /workdir/jupyterhub
RUN mkdir /workdir/jupyterhub/home
RUN mkdir /workdir/jupyterhub/env
RUN mkdir /workdir/notebooks

RUN chgrp -R project /workdir
RUN chmod -R 2775 /workdir

ARG user=jupyterhub
ARG home=/workdir/jupyterhub/home/$user
RUN addgroup --system docker
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home $home \
    --ingroup docker \
    $user


RUN usermod -aG shadow jupyterhub
RUN usermod -aG project jupyterhub

RUN usermod --add-subuids 100000-165535 --add-subgids 100000-165535 jupyterhub

RUN echo "jupyterhub:jupyterhub" | chpasswd

RUN usermod -aG sudo jupyterhub

#RUN groupadd jupyterhub

#RUN usermod -aG jupyterhub jupyterhub

#RUN chown jupyterhub:jupyterhub /workdir

#ensures that /var/run/docker.sock exists
#RUN touch /var/run/docker.sock

#changes the ownership of /var/run/docker.sock
#RUN chown jupyterhub:project /var/run/docker.sock

USER jupyterhub

ARG HOME=/workdir/jupyterhub/

RUN sh /usr/bin/dockerd-rootless-setuptool.sh install --skip-iptables

ENV VIRTUAL_ENV=/workdir/jupyterhub/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN /workdir/jupyterhub/env/bin/pip -q install pip --upgrade

# Install dependencies:
COPY requirements.txt .
RUN /workdir/jupyterhub/env/bin/pip install -r requirements.txt

#RUN jupyter lab build

RUN /workdir/jupyterhub/env/bin/pip -q install wheel

#RUN /workdir/jupyterhub/env/bin/pip install git+https://github.com/manics/podmanclispawner

WORKDIR /workdir/jupyterhub

#RUN touch jupyterhub_cookie_secret
#RUN chmod g+rw jupyterhub_cookie_secret
#RUN openssl rand -hex 32 > jupyterhub_cookie_secret
#RUN chmod 600 jupyterhub_cookie_secret

#RUN jupyterhub --generate-config
COPY jupyterhub_config.py /workdir/jupyterhub/jupyterhub_config.py
#COPY . .
#EXPOSE 8000
CMD . /workdir/jupyterhub/env/bin/activate && exec jupyterhub -f /workdir/jupyterhub/jupyterhub_config.py
