podman exec container_fastapi_alembic_1 alembic init -t async migrations
podman cp alembic.ini /opt/dmtools/code/basecode/fastapi_alembic/app/alembic.ini
podman cp script.py.mako /opt/dmtools/code/basecode/fastapi_alembic/app/migrations/script.py.mako
podman cp env.py /opt/dmtools/code/basecode/fastapi_alembic/app/migrations/env.py
podman exec container_fastapi_alembic_1 alembic revision --autogenerate -m "Initial Commit"
podman exec container_fastapi_alembic_1 alembic upgrade head
