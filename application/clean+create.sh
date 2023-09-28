podman stop container_login_1
podman rm container_login_1
podman rmi login_1

cd /opt/dmtools/code/basecode/application

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman build -f Dockerfile -t application_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_application_1 \
--pod pod_main \
--user $uid:$gid \
-v /opt/dmtools/code/basecode/:/workdir \
localhost/application_1:latest
