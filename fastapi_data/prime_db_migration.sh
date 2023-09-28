podman exec --user agaitske container_fastapi_data_1 alembic init -t async migrations
cp alembic.ini /opt/dmtools/code/basecode/fastapi_data/app/alembic.ini
cp script.py.mako /opt/dmtools/code/basecode/fastapi_data/app/migrations/script.py.mako
cp env.py /opt/dmtools/code/basecode/fastapi_data/app/migrations/env.py
podman exec --user agaitske container_data_alembic_1 alembic revision --autogenerate -m "Initial Commit"
podman exec --user agaitske container_data_alembic_1 alembic upgrade head
