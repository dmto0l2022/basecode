import logging
import mariadb
import asyncmy

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

TORTOISE_ORM = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'mariadb',
            'credentials': {
                'host': '0.0.0.0',
                'port': '5432',
                'user': 'pythonuser',
                'password': 'pythonuser',
                'database': 'dev',
            }
        },
        # Using a DB_URL string
        ##'default': 'postgres://postgres:qwerty123@localhost:5432/events'
    },
    'apps': {
        'models': {
            'models': ["models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
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


# connections is a singleton instance of the ConnectionHandler class and serves as the
# entrypoint to access all connection management APIs.
from tortoise import connections
from tortoise import Tortoise

@app.get("/aerich/connect")
async def connect():
    # Assume that this is the Tortoise configuration used
    
    await Tortoise.init(TORTOISE_ORM)
    '''
     await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example.sqlite3"},
                }
            },
            "apps": {
                "events": {"models": ["__main__"], "default_connection": "default"}
            },
        }
    )
    '''
    conn: BaseDBAsyncClient = connections.get("default")
    try:
        await conn.execute_query('SELECT * FROM "event"')
    except OperationalError:
        print("Expected it to fail")
    return {"conn": "connected!"}
