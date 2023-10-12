uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

podman stop container_fastapi_about_1
podman rm container_fastapi_about_1

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

## fastapi about api

cd /opt/dmtools/code/basecode/fastapi_about

podman rmi fastapi_about_1

podman build \
--build-arg=BUILD_ENV_UID=${ENV_UID} \
--build-arg=BUILD_ENV_USERNAME=${ENV_USERNAME} \
--build-arg=BUILD_ENV_GID=${ENV_GID} \
--build-arg=BUILD_ENV_GROUPNAME=${ENV_GROUPNAME} \
-f Dockerfile -t fastapi_about_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_about_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_about_1:latest
