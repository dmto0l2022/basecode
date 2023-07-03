podman stop container_api_backend_1
# podman stop infra_api_backend
# podman rm container_api_backend_1
#podman rm infra_api_backend

podman pod stop pod_api_backend
podman pod rm pod_api_backend

podman rmi image_pythonapi_1

cd /opt/dmtools/code/flask-mariadb-nginx/flask_crud_api

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman pod create \
--name pod_api_backend \
--infra-name infra_api_backend \
--network bridge \
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
--publish 8004:8004

podman build -f Dockerfile_pythonbase -t image_pythonbaseapi_1 .
podman build -f Dockerfile_pythonapi -t image_pythonapi_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_api_backend_1 \
--pod pod_api_backend \
--user $uid:$gid \
localhost/image_pythonapi_1:latest
