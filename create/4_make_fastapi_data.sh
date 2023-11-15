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
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
-v /opt/dmtools/code/basecode:/workdir \
localhost/fastapi_data_1:latest

cd /opt/dmtools/code/basecode/create

