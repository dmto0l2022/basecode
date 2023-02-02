podman stop container_notebook_1
podman rm container_notebook_1
podman rmi notebook_1

cd /opt/dmtools/code/basecode/notebook

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman build -f Dockerfile -t notebook_1 .

##-v /HOST-DIR:/CONTAINER-DIR
##-v /opt/dmtools/code/basecode/:/workdir \


podman run -dt \
--name container_notebook_1 \
--pod pod_main_backend \
--user $uid:$gid \
localhost/notebook_1:latest

