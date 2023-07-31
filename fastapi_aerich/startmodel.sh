podman exec container_fastapi_aerich_1 aerich init -t aerich.ini
podman exec container_fastapi_aerich_1 aerich init -t db.TORTOISE_ORM -s /app
podman exec container_fastapi_aerich_1 aerich init-db

