uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

cd /opt/dmtools/code/basecode/fastapi_orm

podman stop container_fastapi_orm_1
podman rm container_fastapi_orm_1
podman rmi fastapi_orm_1
podman build -f Dockerfile -t fastapi_orm_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_orm_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_orm_1:latest
