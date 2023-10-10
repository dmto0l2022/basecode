podman stop container_443

podman pod rm pod_main
podman rmi nginx:latest
podman rmi image_nginx443:latest

podman pod create \
--name pod_main \
--infra-name infra_1 \
--network bridge \
--publish 443:443 \
--publish 80:80

podman build -f Dockerfile443 -t image_nginx443 .

## host:container

podman run -dt \
--name container_443 \
--pod pod_main \
-v /etc/pki/nginx:/etc/pki/nginx \
-v /var/www/phetwebcit.services.brown.edu:/var/www \
-v /var/log/nginx/phetwebcit.services.brown.edu:/var/log/nginx/log \
localhost/image_nginx443:latest

#    root         /var/www/phetwebcit.services.brown.edu/:/var/www/
#    access_log   /var/log/nginx/phetwebcit.services.brown.edu/access.log;
#    error_log    /var/log/nginx/phetwebcit.services.brown.edu/error.log;
#    ssl_certificate "/etc/pki/nginx/dmtools_het_brown_edu.pem";
#    ssl_certificate_key "/etc/pki/nginx/private/dmtools.key";
