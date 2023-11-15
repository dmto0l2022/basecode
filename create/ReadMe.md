# Recreate the Full Application

## Set Environmental Variables

## Run main.sh


# ports

8004 api

8002 frontend

# Running Containers

podman exec -it container_fastapi_data_1 /bin/sh

# Permission issues

podman run -v /tmp/data:/data fedora touch /data/content

podman run -v /opt/dmtools/code/basecode/fastapi_data/app:/data fedora touch /data/content  

podman run --privileged -v /opt/dmtools/code/basecode/fastapi_data/app:/data fedora touch /data/content

podman run -v /opt/dmtools/code/basecode/fastapi_data/app:/data:Z fedora touch /data/content  ### Z is important!
