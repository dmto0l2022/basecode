# podman run -it --userns=keep-id registry.access.redhat.com/rhel7/rhel /bin/bash

podman pod stop pod_main_backend
podman pod rm pod_main_backend

uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

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
