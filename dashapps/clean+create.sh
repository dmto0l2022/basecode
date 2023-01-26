podman stop container_dashapps_1
podman rm container_dashapps_1
podman rmi base_dashapps_1
podman rmi dashapps_1

cd /opt/dmtools/code/basecode/dashapps

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman build -f Dockerfile_frontendbase -t base_frontend_1 .
podman build -f Dockerfile_frontend -t dashapps_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_dashapps_1 \
--pod pod_main_backend \
--user $uid:$gid \
-v /opt/dmtools/code/basecode/:/workdir \
localhost/dashapps_1:latest
