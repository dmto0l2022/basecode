#docker run --detach
#--name some-mariadb
#--env MARIADB_USER=example-user
#--env MARIADB_PASSWORD=my_cool_secret
#--env MARIADB_ROOT_PASSWORD=my-secret-pw  
#mariadb:latest

FROM mariadb:latest

RUN apt-get update && apt-get -y install vim
RUN apt-get -y install unzip

ARG ENV_USERNAME=me
ARG ENV_UID=9999
ARG ENV_GID=9999
ARG ENV_GROUPNAME=thegroup
ARG ENV_MARIADB_USER=pythonuser
ARG ENV_MARIADB_PASSWORD=pythonuser
ARG ENV_MARIADB_ROOT_PASSWORD=pythonuser
ARG ENV_MARIADB_DATABASE=world
ARG ENV_LOCALHOST=localhost

RUN echo ${ENV_UID}


ARG USERNAME=${ENV_USERNAME}
ARG USER_UID=${ENV_UID}
ARG USER_GID=${ENV_GID} ##
ARG USER_GROUPNAME=${ENV_GROUPNAME}

# Create the user
RUN echo groupadd --gid ${ENV_GID} ${ENV_GROUPNAME}
RUN groupadd --gid ${ENV_GID} ${ENV_GROUPNAME}
RUN echo useradd --uid ${ENV_UID} --gid ${ENV_GID} -m ${ENV_USERNAME}
RUN useradd --uid ${ENV_UID} --gid ${ENV_GID} -m ${ENV_USERNAME}

   

#RUN mkdir /docker-entrypoint-initdb.d ## already exists
RUN chown $USER_UID:$USER_GID /docker-entrypoint-initdb.d
RUN chown $USER_UID:$USER_GID /var/lib/mysql

USER $USERNAME
#ADD sql/ /docker-entrypoint-initdb.d

#ENV MYSQL_ROOT_PASSWORD test123
#ENV MYSQL_DATABASE testDB
#ENV MYSQL_USER toto
#ENV MYSQL_PASSWORD test123

env MARIADB_USER=${ENV_MARIADB_USER}
env MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD}
env MARIADB_ROOT_PASSWORD=${ENV_MARIADB_ROOT_PASSWORD}
env MARIADB_DATABASE=${ENV_MARIADB_DATABASE}

COPY world-db.zip /var/www/html/world-db.zip
RUN unzip -j /var/www/html/world-db.zip -d /docker-entrypoint-initdb.d

#RUN unzip -j /var/www/html/world-db.zip -d /

### COPY x_backup.sql /docker-entrypoint-initdb.d

#unzip -j /path/to/file.zip -d other_folder

#RUN rm /var/www/html/world-db.zip

COPY init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306

CMD ["mysqld"]

