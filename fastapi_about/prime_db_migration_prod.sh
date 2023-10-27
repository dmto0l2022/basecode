podman exec --user dmtools container_fastapi_about_1 alembic init -t async migrations
cp alembic.ini /opt/dmtools/code/basecode/fastapi_about/app/alembic.ini
cp script.py.mako /opt/dmtools/code/basecode/fastapi_about/app/migrations/script.py.mako
cp env.py /opt/dmtools/code/basecode/fastapi_about/app/migrations/env.py
podman exec --user dmtools container_fastapi_about_1 alembic revision --autogenerate -m "Initial Commit"
podman exec --user dmtools container_fastapi_about_1 alembic upgrade head
