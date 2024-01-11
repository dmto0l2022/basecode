import os
from os import environ, path
from dotenv import load_dotenv

#BASE_DIR = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(BASE_DIR, ".env"))

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
#env_path = path.join(BASE_DIR, "app/.env")
#print("env path >>>>>>>>>>" , env_path)
env_path = "/workdir/fastapi_data/app/.env"
load_dotenv(path.join(env_path))


from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

'''
config = {
    "connections": {"default": "mysql://pythonuser:pythonuser@container_mariadb:3306/data"},
    "apps": {
        "models": {
            "models": ["models.models", "models.metadata", "models.dmtools"],
            "default_connection": "default",
        },
    },
}
'''

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
MARIADB_DATABASE = 'data'
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")


#print(MARIADB_USERNAME)
#print(MARIADB_CONTAINER)
#print(MARIADB_PASSWORD)
#print(MARIADB_DATABASE)

DATABASE_URL = "mysql+aiomysql://" + MARIADB_USERNAME + ':' + MARIADB_PASSWORD + '@' + MARIADB_CONTAINER + ':3306/' + MARIADB_DATABASE

#DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL = "mysql+aiomysql://pythonuser:pythonuser@container_mariadb:3306/data"

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True))

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
