uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

podman stop container_fastapi_aerich_1
podman rm container_fastapi_aerich_1
podman rmi fastapi_aerich_1

cd /opt/dmtools/code/basecode/fastapi_aerich

podman stop container_fastapi_aerich_1
podman rm container_fastapi_aerich_1
podman rmi fastapi_aerich_1
podman build -f Dockerfile -t fastapi_aerich_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_aerich_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_aerich_1:latest
