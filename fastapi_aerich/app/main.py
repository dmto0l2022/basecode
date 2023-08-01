import logging
import mariadb


from db import init_db, init_tortoise
from fastapi import FastAPI

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI(title="DMTOOL API Server",
              openapi_url="/aerich/openapi.json",
              docs_url="/aerich/docs"
             )
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)
    await init_tortoise()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


from aerich import Command

config = {
    "connections": {"default": "mysql://pythonuser:pythonuser@container_mariadb:3306/dev"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

@app.get("/aerich/migrate")
async def migrate():
    command = Command(tortoise_config=config, app='models')
    await command.init()
    await command.migrate('test')
    return {"migrate": "migrated!"}

@app.get("/aerich/ping")
def pong():
    return {"ping": "pong!"}
