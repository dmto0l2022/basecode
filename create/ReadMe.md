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

