uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002


subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))


cd /opt/dmtools/code/basecode/fastapi_data

rm -rf /opt/dmtools/code/basecode/fastapi_data/app/migrations/

podman stop container_fastapi_data_1
podman rm container_fastapi_data_1

podman rmi fastapi_data_1

## --build-arg=BUILD_ENV_GROUPNAME=${ENV_GROUPNAME} \

podman build \
--build-arg=BUILD_ENV_UID=${ENV_UID} \
--build-arg=BUILD_ENV_USERNAME=${ENV_USERNAME} \
--build-arg=BUILD_ENV_GID=${ENV_GID} \
--build-arg=BUILD_ENV_GROUPNAME=${ENV_GROUPNAME} \
-f Dockerfile -t fastapi_data_1

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_fastapi_data_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir:Z \
localhost/fastapi_data_1:latest

cd /opt/dmtools/code/basecode/create

