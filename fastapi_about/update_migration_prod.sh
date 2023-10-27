timestamp=$(date +%Y%m%d%H%M%S%N)
podman exec --user dmtools container_fastapi_about_1 alembic revision --autogenerate -m $timestamp
podman exec --user dmtools container_fastapi_about_1 alembic upgrade head
