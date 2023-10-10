podman stop container_443dev

podman rm container_443dev

podman pod rm pod_networking_1
podman rm infra_networking_1

podman rmi nginx:latest
podman rmi image_nginx443dev:latest


podman pod create \
--name pod_networking_1 \
--infra-name infra_networking_1 \
--network bridge \
--publish 443:443 \
--publish 80:80

podman build -f Dockerfile443dev -t image_nginx443dev .

##-v /HOST-DIR:/CONTAINER-DIR

## host:container

podman run -dt \
--name container_443dev \
--pod pod_networking_1 \
-v /etc/letsencrypt:/etc/letsencrypt \
localhost/image_nginx443dev:latest
