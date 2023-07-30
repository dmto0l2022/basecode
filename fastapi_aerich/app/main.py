import logging

from db import init_db
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


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
