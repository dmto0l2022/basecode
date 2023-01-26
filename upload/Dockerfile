#FROM python:3.10.9-slim-bullseye
##3.10.9-slim-bullseye, 3.10-slim-bullseye, 3.10.9-slim, 3.10-slim
FROM python:3
RUN apt-get update && apt-get -y install vim
RUN apt-get -y install unzip

RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get update && apt-get install -y mariadb-server galera-4 mariadb-client libmariadb3 mariadb-backup mariadb-common
RUN apt-get install -y libmariadb-dev

WORKDIR /workdir

ARG USERNAME=agaitske
ARG USER_UID=1001
ARG USER_GID=1002 ## dm group

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

#RUN mkdir /docker-entrypoint-initdb.d ## already exists
#RUN chown $USER_UID:$USER_GID /docker-entrypoint-initdb.d
#RUN chown $USER_UID:$USER_GID /var/lib/mysql
RUN chown $USER_UID:$USER_GID /workdir

RUN mkdir /workdir/uploads
RUN chown $USER_UID:$USER_GID /workdir/uploads

USER $USERNAME

## https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

ENV VIRTUAL_ENV=/workdir/app/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
##COPY requirements.txt .
##RUN pip install -r requirements.txt

# Run the application:
#COPY myapp.py .
#CMD ["python", "myapp.py"]


##RUN python3 -m venv /app/env
##RUN /app/env/bin/python -m pip install --upgrade pip
RUN /workdir/app/env/bin/python3 -m pip install --upgrade pip
RUN . /workdir/app/env/bin/activate
RUN /workdir/app/env/bin/python3 --version
RUN whereis python3
RUN whereis pip3
COPY requirements.txt /workdir/requirements.txt
RUN /workdir/app/env/bin/pip3 install -r /workdir/requirements.txt
RUN /workdir/app/env/bin/pip3 freeze
COPY . /workdir/.
##RUN ls -R /workdir/
EXPOSE 8002
##CMD [ "/app/env/bin/python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8002"]
##RUN chmod +x //app/entry-point.sh
ENTRYPOINT ["sh","/workdir/entry-point.sh"]
