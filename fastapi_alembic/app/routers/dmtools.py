from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

from models.dmtools import Experiment, ExperimentCreate
from models.dmtools import Limit_display, Limit_displayCreate
from models.dmtools import Limit_ownership, Limit_ownershipCreate
from models.dmtools import Limits, LimitsCreate
from models.dmtools import Plot_ownership, Plot_ownershipCreate
from models.dmtools import Plots, PlotsCreate

# Experiment CRUD

@router.get("/alembic/experiments", response_model=list[Experiment])
async def get_experiments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Experiment))
    experiment = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]


@router.post("/alembic/experiments")
async def add_experiment(experiment: ExperimentCreate, session: AsyncSession = Depends(get_session)):
    experiment = Experiment(name=experiment.name, id=experiment.id)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment

@router.delete("/alembic/experiments/{experiment_id}")
async def delete_experiment(experiment_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Experiment).where(Experiment.id == experiment_id)
    results = await session.exec(statement)
    experiment = results.one()
    await session.delete(experiment)
    await session.commit()
    return {"deleted": experiment}


