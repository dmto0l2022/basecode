podman stop container_8080
podman stop container_8090
podman stop container_443dev

podman pod rm pod_main
podman rmi nginx:latest
podman rmi image_nginx443dev:latest
podman rmi image_nginx8080:latest
podman rmi image_nginx8090:latest


podman pod create \
--name pod_main \
--infra-name infra_1 \
--network bridge \
--publish 443:443 \
--publish 80:80

podman build -f Dockerfile443dev -t image_nginx443dev .
podman build -f Dockerfile8080 -t image_nginx8080 .
podman build -f Dockerfile8090 -t image_nginx8090 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_8080 \
--pod pod_main \
localhost/image_nginx8080:latest

podman run -dt \
--name container_8090 \
--pod pod_main \
localhost/image_nginx8090:latest

## host:container

podman run -dt \
--name container_443dev \
--pod pod_main \
-v /etc/letsencrypt:/etc/letsencrypt \
localhost/image_nginx443dev:latest
