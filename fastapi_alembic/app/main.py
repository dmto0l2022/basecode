from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session, init_db

#from routers import routers
from routers import songs
from routers import users
from routers import dmtools
from routers import metadata

app = FastAPI(title="DMTOOL API Server - Alembic",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url="/alembic/openapi.json",
              docs_url="/alembic/docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )

app.include_router(routers.router)
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(dmtools.router)
app.include_router(metadata.router)

