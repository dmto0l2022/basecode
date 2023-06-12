# podman run -it --userns=keep-id registry.access.redhat.com/rhel7/rhel /bin/bash

podman pod stop pod_main_backend
podman pod rm pod_main_backend

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

# as root inside

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--userns=keep-id \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--uidmap 0:1:$uid \
#--uidmap $uid:0:1 \
#--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
#--gidmap 0:1:$gid \
#--gidmap $gid:0:1 \
#--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379

podman pod create \
--name pod_main_backend \
--infra-name infra_main_backend \
--network bridge \
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
--publish 8002 \
--publish 8004:8004 \
--publish 8006 \
--publish 8008 \
--publish 3306 \
--publish 6379

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--userns=keep-id:uid=1001,gid=1002 \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379

##-v /HOST-DIR:/CONTAINER-DIR

cd /opt/dmtools/code/basecode/redis
podman stop container_redis_1
podman rm container_redis_1
podman rmi redis_1

podman build -f Dockerfile -t redis_1 .

#podman pull docker.io/dmto0l2022/redis_1:latest

### remember to create this on host
### /opt/dmtools/redis-data

podman volume rm redis-data

podman volume create redis-data

podman run -dt \
--name container_redis_1 \
--pod pod_main_backend \
--user $uid:$gid \
--volume redis-data:/data \
localhost/redis_1:latest

##--volume /opt/dmtools/redis-data:/data \

cd /opt/dmtools/code/basecode/mariadb
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
--volume /opt/dmtools/mysql:/var/lib/mysql:z \
localhost/mariadb_1:latest

## --volume /opt/dmtools/mysql:/var/lib/mysql:z \
## --volume mariadb_data:/var/lib/mysql \

##### --env MARIADB_USER=${ENV_MARIADB_USER} --env MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} --env MARIADB_ROOT_PASSWORD=${ENV_MARIADB_PASSWORD} \

cd /opt/dmtools/code/basecode/api

podman rmi api_1
podman rmi base_api_1
podman build -f Dockerfile_apibase -t base_api_1
podman build -f Dockerfile_api -t api_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_api_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/api_1:latest

###

cd /opt/dmtools/code/basecode/fastapi

podman rmi fastapi_1
podman build -f Dockerfile -t fastapi_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_1:latest

####

cd /opt/dmtools/code/basecode/fastapi_orm

podman rmi fastapi_orm_1
podman build -f Dockerfile -t fastapi_orm_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_orm_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_orm_1:latest

####

cd /opt/dmtools/code/basecode/frontend

podman rmi frontend_1:latest
podman build -f Dockerfile_frontendbase -t base_frontend_1 .
podman build -f Dockerfile_frontend -t frontend_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_frontend_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/frontend_1:latest



