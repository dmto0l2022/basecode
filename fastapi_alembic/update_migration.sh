timestamp=$(date +%Y%m%d%H%M%S%N)
podman exec container_fastapi_alembic_1 alembic revision --autogenerate -m timestamp
podman exec container_fastapi_alembic_1 alembic upgrade head
