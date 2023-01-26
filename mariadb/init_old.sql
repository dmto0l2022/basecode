CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'pythonuser';

CREATE DATABASE data;

GRANT ALL PRIVILEGES ON *.* TO 'pythonuser'@'localhost' WITH GRANT OPTION;

ALTER USER 'pythonuser'@'%' IDENTIFIED BY 'pythonuser';

##ALTER USER 'pythonuser'@'%' IDENTIFIED WITH mysql_native_password BY 'pythonuser';

##ALTER USER root@localhost IDENTIFIED BY PASSWORD '************';

##ALTER USER 'pythonuser'@'%' IDENTIFIED BY PASSWORD 'pythonuser';

## create user pythonuser@'%' identified by 'pythonuser'; ## used this when logged into MariaDB Server

##GRANT ALL PRIVILEGES ON *.* TO pythonuser@'%' WITH GRANT OPTION; ## used this when logged into MariaDB Server

GRANT ALL PRIVILEGES ON *.* TO 'pythonuser'@'%' WITH GRANT OPTION; ## This is required when using Dockerfile
