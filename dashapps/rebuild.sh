id=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))


podman stop container_frontend_1
podman rm container_frontend_1
podman rmi frontend_1

podman build -f Dockerfile_frontend -t frontend_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_frontend_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode:/workdir \
localhost/frontend_1:latest

