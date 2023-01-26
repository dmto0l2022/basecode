podman pod stop pod_main_backend
podman pod rm pod_main_backend

uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

cd /opt/dmtools/code/flask-mariadb-nginx/redis
podman stop container_redis_1

#podman pull docker.io/dmto0l2022/redis_1:latest

podman rmi redis_1
podman build -f Dockerfile -t redis_1 .

podman run -dt \
--name container_redis_1 \
--user $uid:$gid \
localhost/redis_1:latest

cd /opt/dmtools/code/flask-mariadb-nginx/mariadb
podman rmi mariadb_1

podman build \
--build-arg=ENV_UID=${ENV_UID} \
--build-arg=ENV_USERNAME=${ENV_USERNAME} \
--build-arg=ENV_GID=${ENV_GID} \
--build-arg=ENV_GROUPNAME=${ENV_GROUPNAME} \
--build-arg=ENV_MARIADB_USER=${ENV_MARIADB_USER} \
--build-arg=ENV_MARIADB_PASSWORD=${ENV_MARIADB_PASSWORD} \
--build-arg=ENV_MARIADB_ROOT_PASSWORD=${ENV_MARIADB_ROOT_PASSWORD} \
--build-arg=ENV_MARIADB_DATABASE=${ENV_MARIADB_DATABASE} \
-t mariadb_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_mariadb_backend \
--volume /opt/dmtools/mysql:/var/lib/mysql:z \
--user $uid:$gid \
localhost/mariadb_1:latest

cd /opt/dmtools/code/flask-mariadb-nginx/flask_crud_api

podman rmi image_python_api_1
podman build -f Dockerfile_pythonapi -t image_python_api_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_api_backend_1 \
--user $uid:$gid \
localhost/python_api_1:latest

cd /opt/dmtools/code/flask-mariadb-nginx/flask_dash_frontend

podman rmi flask_dash_frontend_1:latest
podman build -f Dockerfile_pythonfrontend -t flask_dash_frontend_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_flask_dash_frontend_1 \
--user $uid:$gid \
localhost/flask_dash_frontend_1:latest

