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

rm -rf /data/containers/data/backups/mysql
mkdir /data/containers/data/backups/mysql

cd /opt/dmtools/code/basecode/backup_db

podman stop container_backup_db
podman rm container_backup_db
podman rmi backup_db_1

podman build \
--build-arg=BUILD_ENV_UID=${ENV_UID} \
--build-arg=BUILD_ENV_USERNAME=${ENV_USERNAME} \
--build-arg=BUILD_ENV_GID=${ENV_GID} \
--build-arg=BUILD_ENV_GROUPNAME=${ENV_GROUPNAME} \
--build-arg=BUILD_ENV_MARIADB_USER=${ENV_MARIADB_USER} \
--build-arg=BUILD_ENV_MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} \
--build-arg=BUILD_ENV_MARIADB_ROOT_PASSWORD=${ENV_MARIADB_ROOT_PASSWORD} \
--build-arg=BUILD_ENV_MARIADB_DATABASE=${ENV_MARIADB_DATABASE} \
-t backup_db_1 .

##-v /HOST-DIR:/CONTAINER-DIR

## --env MARIADB_USER=example-user --env MARIADB_PASSWORD=my_cool_secret --env MARIADB_ROOT_PASSWORD=my-secret-pw 

podman run -dt \
--name container_mariadb \
--pod pod_main_backend \
--user $uid:$gid \
--log-opt max-size=10mb \
--volume /data/containers/data/backups/mysql:/var/lib/mysql:z \
localhost/backup_db_1:latest

## --volume /opt/dmtools/mysql:/var/lib/mysql:z \
## --volume mariadb_data:/var/lib/mysql \

##### --env MARIADB_USER=${ENV_MARIADB_USER} --env MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} --env MARIADB_ROOT_PASSWORD=${ENV_MARIADB_PASSWORD} \

cd /opt/dmtools/code/basecode/create
