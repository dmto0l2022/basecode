id=${ENV_UID} ##1001
gid=${ENV_GID} ##1002

cd /opt/dmtools/code/basecode/fastapi

podman stop container_mariadb
podman rm container_mariadb
podman rmi mariadb_1

