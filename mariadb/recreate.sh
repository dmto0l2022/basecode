id=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

cd /opt/dmtools/code/basecode/mariadb

podman stop container_mariadb
podman rm container_mariadb
podman rmi mariadb_1


#podman build \
#--build-arg=BUILD_ENV_MARIADB_USER=${ENV_MARIADB_USER} \
#--build-arg=BUILD_ENV_MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} \
#--build-arg=BUILD_ENV_MARIADB_ROOT_PASSWORD=${ENV_MARIADB_ROOT_PASSWORD} \
#--build-arg=BUILD_ENV_MARIADB_DATABASE=${ENV_MARIADB_DATABASE} \
#-t mariadb_1 .

#podman build -t mariadb_1 .

# https://www.baeldung.com/ops/dockerfile-env-variable

podman build \
--build-arg=BUILD_ENV_UID=${ENV_UID} \
--build-arg=BUILD_ENV_USERNAME=${ENV_USERNAME} \
--build-arg=BUILD_ENV_GID=${ENV_GID} \
--build-arg=BUILD_ENV_GROUPNAME=${ENV_GROUPNAME} \
--build-arg=BUILD_ENV_MARIADB_USER=${ENV_MARIADB_USER} \
--build-arg=BUILD_ENV_MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} \
--build-arg=BUILD_ENV_MARIADB_ROOT_PASSWORD=${ENV_MARIADB_ROOT_PASSWORD} \
--build-arg=BUILD_ENV_MARIADB_DATABASE=${ENV_MARIADB_DATABASE} \
-t mariadb_1 .

##-v /HOST-DIR:/CONTAINER-DIR

## --env MARIADB_USER=example-user --env MARIADB_PASSWORD=my_cool_secret --env MARIADB_ROOT_PASSWORD=my-secret-pw 

podman run -dt \
--name container_mariadb \
--pod pod_main_backend \
--user $uid:$gid \
--volume /data/containers/data/mysql:/var/lib/mysql:z \
localhost/mariadb_1:latest

## --volume /opt/dmtools/mysql:/var/lib/mysql:z \
## --volume mariadb_data:/var/lib/mysql \

##### --env MARIADB_USER=${ENV_MARIADB_USER} --env MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} --env MARIADB_ROOT_PASSWORD=${ENV_MARIADB_PASSWORD} \
