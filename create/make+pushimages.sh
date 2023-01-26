#creating following docker.io repositories
#redis_1
#python_base_api_1
#python_base_frontend_1

cd /opt/dmtools/code/flask-mariadb-nginx/redis
podman rmi redis_1:latest
podman build -f Dockerfile -t redis_1 .
#podman tag redis_1:latest dmto0l2022/redis_1:latest
podman push redis_1:latest dmto0l2022/redis_1:latest

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

## not pushing the above for obvious reasons!

#podman stop container_api_backend_1
podman rmi python_base_api_1
podman rmi python_api_1
cd /opt/dmtools/code/flask-mariadb-nginx/flask_crud_api

podman build -f Dockerfile_pythonbase -t python_base_api_1 .
podman push python_base_api_1:latest dmto0l2022/python_base_api_1:latest

## this is only local as it contains the env file
podman build -f Dockerfile_pythonapi -t python_api_1 .

podman stop container_flask_dash_frontend_1
podman rmi python_base_frontend_1
podman rmi flask_dash_frontend_1

cd /opt/dmtools/code/flask-mariadb-nginx/flask_dash_frontend

podman build -f Dockerfile_pythonfrontendbase -t python_base_frontend_1 .
podman push python_base_frontend_1:latest dmto0l2022/python_base_frontend_1:latest

## this is only local as it contains the env file
podman build -f Dockerfile_pythonfrontend -t flask_dash_frontend_1 .


