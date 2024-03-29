import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from sqlmodel import SQLModel

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
from models.users import User, User_permission, User_api_key
from models.base import Base
target_metadata = Base.metadata
#target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

from os import environ, path

from dotenv import load_dotenv


BASE_DIR = path.abspath(path.dirname(__file__))
#env_path = path.join(BASE_DIR, "app/.env")
#print("env path >>>>>>>>>>" , env_path)
env_path = "/workdir/fastapi_about/app/.env"
load_dotenv(path.join(env_path))

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
#MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_DATABASE = 'about'
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")


DATABASE_URL = "mysql+aiomysql://" + MARIADB_USERNAME + ":" + \
                MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                + MARIADB_DATABASE

print(DATABASE_URL)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    #url = config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    #connectable = async_engine_from_config(
    #    config.get_section(config.config_ini_section, {}),
    #    prefix="sqlalchemy.",
    #    poolclass=pool.NullPool,
    #)

    connectable = create_async_engine(DATABASE_URL)
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    print("<<<<<< run_migrations_offline() >>>>>>>>>")
    run_migrations_offline()
else:
    print("<<<<<< run_migrations_online() >>>>>>>>>")
    run_migrations_online()
