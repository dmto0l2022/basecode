podman pod stop frontend
podman pod rm frontend
podman rmi -a

## docker run -p 3306:3306 -d --name mariadb -e MARIADB_ROOT_PASSWORD=Password123! mariadb/server:10.4 
## podman run -dt --pod new:frontend -p 3306:3306 localhost/my-mariadb-1:latest

podman pod create \
--name frontend \
--publish 3306:3306

#env MARIADB_USER=pythonuser
#env MARIADB_PASSWORD=pythonuser
#env MARIADB_ROOT_PASSWORD=pythonuser
#env MARIADB_DATABASE=world

podman run --detach \
--pod frontend \
--restart=always \
-e MARIADB_ROOT_PASSWORD="pythonuser" \
-e MARIADB_DATABASE="world" \
-e MARIADB_USER="pythonuser" \
-e MARIADB_PASSWORD="pythonuser" \
-e MARIADB_ROOT_HOST="localhost" \
--name=mariadb1 mariadb

##podman run -dt --pod new:frontend -p 3306:3306 -e MARIADB_ROOT_PASSWORD=Password123! mariadb/server:10.4

podman pod start frontend
