# Using Env file

https://zwbetz.com/set-environment-variables-in-your-bash-shell-from-a-env-file/


# Source of Database

https://dev.mysql.com/doc/index-other.html

# Dbeaver Upgrade

sudo apt install /home/andrewcgaitskell/Downloads/dbeaver-ce_22.3.0_amd64.deb


# Dockerfile Notes

https://mariadb.com/kb/en/creating-a-custom-docker-image/


Using Variables

It is possible to use variables in a Dockerfile. This allows us, for example, to install different packages, install different versions of a package, or configure software differently depending on how variables are set, without modifying the Dockerfile itself.

To use a variable, we can do something like this:

FROM ubuntu:20.04

ARG MARIADB_CONFIG_FILE

...

RUN mysqld --defaults-file=$MARIADB_CONFIG_FILE

Here ARG is used after the FROM directive, thus the variable cannot be used in FROM. It is also possible to declare a variable before FROM, so we can use a variable to select the base image to use or its tag, but in this case the variable cannot be used after the FROM directive. Here is an example:

ARG UBUNTU_VERSION
FROM ubuntu:$UBUNTU_VERSION

# But this will cause a build error:
RUN echo 'Ubuntu version: $UBUNTU_VERSION' > /var/build_log

We'll have to assign variables a value when we build the Dockerfile, in this way:

docker build --build-arg UBUNTU_VERSION=20.04 .

Note that Dockerfile variables are just placeholders for values. Dockerfiles do not support assignment, conditionals or loops.
