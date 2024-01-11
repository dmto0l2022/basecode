uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002
#uid=1001
#gid=1002
#env_username=${ENV_USERNAME}
#env_groupname=${ENV_GROUPNAME}

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

rm -rf /data/containers/data/mysql
mkdir /data/containers/data/mysql

rm /opt/dmtools/code/basecode/mariadb/x_20211104_dmtools_backup.sql


## added x to name so it is executed after init.sql
cp /home/dmtools/download_file/20211104_dmtools_backup.sql /opt/dmtools/code/basecode/mariadb/x_20211104_dmtools_backup.sql

cd /opt/dmtools/code/basecode/mariadb

podman stop container_mariadb
podman rm container_mariadb
podman rmi mariadb_1

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
--log-opt max-size=10mb \
--volume /data/containers/data/mysql:/var/lib/mysql:z \
--volume /data/containers/data/backups:/data/backups:z \
localhost/mariadb_1:latest

## --volume /opt/dmtools/mysql:/var/lib/mysql:z \
## --volume mariadb_data:/var/lib/mysql \

##### --env MARIADB_USER=${ENV_MARIADB_USER} --env MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} --env MARIADB_ROOT_PASSWORD=${ENV_MARIADB_PASSWORD} \

cd /opt/dmtools/code/basecode/create
