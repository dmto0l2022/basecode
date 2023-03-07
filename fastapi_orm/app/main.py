# pylint: disable=E0611,E0401
import os
from os import environ, path

from dotenv import load_dotenv

import secrets
import string
import random

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

from typing import List

from fastapi import FastAPI, HTTPException

from models import Experiment_Pydantic, ExperimentIn_Pydantic, Experiments
from models import Limit_Display_Pydantic, Limit_DisplayIn_Pydantic, Limit_Display
from models import Limit_Ownership_Pydantic, Limit_OwnershipIn_Pydantic, Limit_Ownership   
from models import Limit_Pydantic, LimitIn_Pydantic, Limits
from models import Plot_Ownership_Pydantic, Plot_OwnershipIn_Pydantic, Plot_Ownership
from models import Plot_Pydantic, PlotIn_Pydantic, Plots

from models import User_Pydantic, UserIn_Pydantic, Users




from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI(title="Tortoise ORM FastAPI example")


class Status(BaseModel):
    message: str

#### experiments #####

@app.get("/apiorm/experiments", response_model=List[Experiment_Pydantic])
async def get_experiments():
    return await Experiment_Pydantic.from_queryset(Experiments.all())

@app.post("/apiorm/experiments", response_model=Experiment_Pydantic)
async def create_user(experiment: ExperimentIn_Pydantic):
    experiment_obj = await Experiments.create(**experiment.dict(exclude_unset=True))
    return await Experiment_Pydantic.from_tortoise_orm(experiment_obj)

@app.get(
    "/apiorm/experiment/{experiment_id}", response_model=Experiment_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_experiment(experiment_id: int):
    return await Experiment_Pydantic.from_queryset_single(Experiment.get(id=experiment_id))

@app.put(
    "/apiorm/experiment/{experiment_id}", response_model=Experiment_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_experiment(experiment_id: int, user: ExperimentIn_Pydantic):
    await Experiments.filter(id=experiment_id).update(**experiment.dict(exclude_unset=True))
    return await Experiment_Pydantic.from_queryset_single(Experiments.get(id=experiment_id))


@app.delete("/apiorm/experiment/{experiment_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_experiment(experiment_id: int):
    deleted_count = await Experiments.filter(id=experiment_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Experiment {experiment_id} not found")
    return Status(message=f"Deleted experiment {experiment_id}")

#### users #####

@app.get("/apiorm/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@app.post("/apiorm/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get(
    "/apiorm/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.put(
    "/apiorm/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.delete("/apiorm/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
MARIADB_DATABASE = environ.get("MARIADB_TEST")
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

MARIADB_URI = "mysql://" + MARIADB_USERNAME + ":" + \
                MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                + MARIADB_DATABASE

print(MARIADB_URI)


register_tortoise(
    app,
    db_url=MARIADB_URI,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
