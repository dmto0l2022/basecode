podman stop container_dmtool80

podman pod rm pod_main80
podman rmi nginx:latest
podman rmi image_nginx_dmtool80:latest

podman pod create \
--name pod_main80 \
--infra-name infra_1 \
--network bridge \
--publish 80:80

podman build -f DockerfileDMTOOL80 -t image_nginx_dmtool80 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_dmtool80 \
--pod pod_main80 \
localhost/image_nginx_dmtool80:latest
