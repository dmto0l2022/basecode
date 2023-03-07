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

#### plot #####

@app.get("/apiorm/plots", response_model=List[Plot_Pydantic])
async def get_plots():
    return await Plot_Pydantic.from_queryset(Plots.all())

@app.post("/apiorm/plot", response_model=Plot_Pydantic)
async def create_plot(plot: PlotIn_Pydantic):
    plot_obj = await Plots.create(**plot.dict(exclude_unset=True))
    return await Plot_Pydantic.from_tortoise_orm(plot_obj)

@app.get(
    "/apiorm/plot/{plot_id}", response_model=Plot_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_plot(plot_id: int):
    return await Plot_Pydantic.from_queryset_single(Plot.get(id=plot_id))

@app.put(
    "/apiorm/plot/{plot_id}", response_model=Plot_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_plot(plot_id: int, plot: PlotIn_Pydantic):
    await Plots.filter(id=plot_id).update(**Plot.dict(exclude_unset=True))
    return await Plot_Pydantic.from_queryset_single(Plot.get(id=plot_id))

@app.delete("/apiorm/plot/{plot_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_plot(plot_id: int):
    deleted_count = await Plot.filter(id=plot_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Plot {plot_id} not found")
    return Status(message=f"Deleted Plot {plot_id}")                   
        
        
#### plot ownership #####

@app.get("/apiorm/plot_ownerships", response_model=List[Plot_Ownership_Pydantic])
async def get_plot_ownerships():
    return await Plot_Ownership_Pydantic.from_queryset(Limit.all())

@app.post("/apiorm/plot_ownership", response_model=Plot_Ownership_Pydantic)
async def create_plot_ownership(plot_ownership: Plot_OwnershipIn_Pydantic):
    plot_ownership_obj = await Plot_Ownership.create(**plot_ownership.dict(exclude_unset=True))
    return await Plot_Ownership_Pydantic.from_tortoise_orm(plot_ownership_obj)

@app.get(
    "/apiorm/plot_ownership/{plot_ownership_id}", response_model=Plot_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_plot_ownership(plot_ownership_id: int):
    return await Plot_Ownership_Pydantic.from_queryset_single(Plot_Ownership.get(id=plot_ownership_id))

@app.put(
    "/apiorm/plot_ownership/{plot_ownership_id}", response_model=Plot_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_plot_ownership(plot_ownership_id: int, plot_ownership: Plot_OwnershipIn_Pydantic):
    await Plot_Ownership.filter(id=plot_ownership_id).update(**Plot_Ownership.dict(exclude_unset=True))
    return await Plot_Ownership_Pydantic.from_queryset_single(Plot_Ownership.get(id=plot_ownership_id))


@app.delete("/apiorm/plot_ownership/{plot_ownership_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit(plot_ownership_id: int):
    deleted_count = await Plot_Ownership.filter(id=plot_ownership_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Plot Ownership {plot_ownership_id} not found")
    return Status(message=f"Deleted Plot Ownership {plot_ownership_id}")        
        
            
        
#### limit #####

@app.get("/apiorm/limit", response_model=List[Limit_Pydantic])
async def get_limits():
    return await Limit_Pydantic.from_queryset(Limit.all())

@app.post("/apiorm/limit", response_model=Limit_Pydantic)
async def create_limit_ownership(limit: LimitIn_Pydantic):
    limit_obj = await Limits.create(**limit.dict(exclude_unset=True))
    return await Limit_Pydantic.from_tortoise_orm(limit_obj)

@app.get(
    "/apiorm/limit/{limit_id}", response_model=Limit_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit(limit_id: int):
    return await Limit_Pydantic.from_queryset_single(Limit.get(id=limit_id))

@app.put(
    "/apiorm/limit/{limit_id}", response_model=Limit_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit(limit_id: int, limit: LimitIn_Pydantic):
    await Limits.filter(id=limit_id).update(**Limit.dict(exclude_unset=True))
    return await Limit_Pydantic.from_queryset_single(Limit.get(id=limit_id))


@app.delete("/apiorm/limit/{limit_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit(limit_id: int):
    deleted_count = await Limit_Ownership.filter(id=limit_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit {limit_id} not found")
    return Status(message=f"Deleted Limit {limit_id}")        
        
   
        
#### limit ownership #####

@app.get("/apiorm/limit_ownership", response_model=List[Limit_Ownership_Pydantic])
async def get_limit_ownerships():
    return await Limit_Ownership_Pydantic.from_queryset(Limit_Ownership.all())

@app.post("/apiorm/limit_ownership", response_model=Limit_Ownership_Pydantic)
async def create_limit_ownership(limit_ownership: Limit_OwnershipIn_Pydantic):
    limit_ownership_obj = await Limit_Ownership.create(**limit_ownership.dict(exclude_unset=True))
    return await Limit_Ownership_Pydantic.from_tortoise_orm(limit_ownership_obj)

@app.get(
    "/apiorm/limit_ownership/{limit_ownership_id}", response_model=Limit_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit_ownership(limit_ownership_id: int):
    return await Limit_Ownership_Pydantic.from_queryset_single(Limit_Ownership.get(id=limit_ownership_id))

@app.put(
    "/apiorm/limit_ownership/{limit_ownership_id}", response_model=Limit_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit_ownership(limit_ownership_id: int, limit_ownership: Limit_OwnershipIn_Pydantic):
    await Limit_Ownership.filter(id=limit_ownership_id).update(**Limit_Ownership.dict(exclude_unset=True))
    return await Limit_Ownership_Pydantic.from_queryset_single(Limit_Ownership.get(id=limit_ownership_id))


@app.delete("/apiorm/limit_ownership/{limit_ownership_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit_ownership(limit_display_id: int):
    deleted_count = await Limit_Ownership.filter(id=limit_display_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit Ownership {limit_ownership_id} not found")
    return Status(message=f"Deleted Limit Ownership {limit_ownership_id}")        
        
#### limit display #####

@app.get("/apiorm/limit_display", response_model=List[Limit_Display_Pydantic])
async def get_limit_displays():
    return await Limit_Display_Pydantic.from_queryset(Limit_Display.all())

@app.post("/apiorm/limit_display", response_model=Limit_Display_Pydantic)
async def create_limit_display(limit_display: Limit_DisplayIn_Pydantic):
    limit_display_obj = await Limit_Display.create(**limit_display.dict(exclude_unset=True))
    return await Limit_Display_Pydantic.from_tortoise_orm(limit_display_obj)

@app.get(
    "/apiorm/limit_display/{limit_display_id}", response_model=Limit_Display_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit_display(limit_display_id: int):
    return await Limit_Display_Pydantic.from_queryset_single(Limit_Display.get(id=limit_display_id))

@app.put(
    "/apiorm/limit_display/{limit_display_id}", response_model=Limit_Display_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit_display(limit_display_id: int, limit_display: Limit_DisplayIn_Pydantic):
    await Limit_Display.filter(id=limit_display_id).update(**Limit_Display.dict(exclude_unset=True))
    return await Limit_Display_Pydantic.from_queryset_single(Limit_Display.get(id=experiment_id))


@app.delete("/apiorm/limit_display/{experiment_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit_display(limit_display_id: int):
    deleted_count = await Limit_Display.filter(id=limit_display_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit Display {limit_display_id} not found")
    return Status(message=f"Deleted experiment {limit_display_id}")        
        
#### experiments #####

@app.get("/apiorm/experiments", response_model=List[Experiment_Pydantic])
async def get_experiments():
    return await Experiment_Pydantic.from_queryset(Experiments.all())

@app.post("/apiorm/experiments", response_model=Experiment_Pydantic)
async def create_experiment(experiment: ExperimentIn_Pydantic):
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
async def update_experiment(experiment_id: int, experiment: ExperimentIn_Pydantic):
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
