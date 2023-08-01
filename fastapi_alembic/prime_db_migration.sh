podman exec container_fastapi_alembic_1 alembic init -t async migrations
podman cp alembic.ini container_fastapi_alembic_1://app/alembic.ini
podman cp script.py.mako container_fastapi_alembic_1://app/migrations/script.py.mako
podman cp env.py container_fastapi_alembic_1://app/migrations/env.py
podman exec container_fastapi_alembic_1 alembic revision --autogenerate -m "Initial Commit"
podman exec container_fastapi_alembic_1 alembic upgrade head
