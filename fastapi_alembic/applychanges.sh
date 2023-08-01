podman exec container_fastapi_alembic_1 alembic revision --autogenerate -m "apply initial commit"
podman exec container_fastapi_alembic_1 alembic alembic upgrade head
