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
from models.dmtools import Limit, LimitCreate
from models.dmtools import Plot_ownership, Plot_ownershipCreate
from models.dmtools import Plot, PlotCreate

# Experiment CRUD

@router.get("/alembic/experiment", response_model=list[Experiment])
async def get_experiment(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Experiment))
    experiments = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]


@router.post("/alembic/experiment")
async def add_experiment(experiment: ExperimentCreate, session: AsyncSession = Depends(get_session)):
    experiment = Experiment(name=experiment.name)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment

@router.delete("/alembic/experiment/{experiment_id}")
async def delete_experiment(experiment_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Experiment).where(Experiment.id == experiment_id)
    results = await session.exec(statement)
    experiment = results.one()
    await session.delete(experiment)
    await session.commit()
    return {"deleted": experiment}


# Limit Display CRUD
## Limit_display, Limit_displayCreate

# Fields
#    id
#    name
#    limit_id
#    plot_id
#    trace_id
#    symbol
#    symbol_color
#    line_style
#    line_color
#    fill_color
#    color
#    style
#    created_at
#    updated_at

@router.get("/alembic/limit_display", response_model=list[Limit_display])
async def get_limit_display(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Limit_display))
    limit_displays = result.scalars().all()
    return [Limit_display(
                        limit_display.id,
                        limit_display.name,
                        limit_display.limit_id,
                        limit_display.plot_id,
                        limit_display.trace_id,
                        limit_display.symbol,
                        limit_display.symbol_color,
                        limit_display.line_style,
                        limit_display.line_color,
                        limit_display.fill_color,
                        limit_display.color,
                        limit_display.style,
                        limit_display.created_at,
                        limit_display.updated_at)
            for limit_display in limit_displays]


@router.post("/alembic/limit_display")
async def add_limit_display(limit_display: Limit_displayCreate, session: AsyncSession = Depends(get_session)):
    limit_display = Limit_display(
                        limit_display.name,
                        limit_display.limit_id,
                        limit_display.plot_id,
                        limit_display.trace_id,
                        limit_display.symbol,
                        limit_display.symbol_color,
                        limit_display.line_style,
                        limit_display.line_color,
                        limit_display.fill_color,
                        limit_display.color,
                        limit_display.style,
                        limit_display.created_at,
                        limit_display.updated_at
                        )
    session.add(limit_display)
    await session.commit()
    await session.refresh(limit_display)
    return limit_display

@router.delete("/alembic/limit_display/{limit_display_id}")
async def delete_limit_display(limit_display_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Limit_display).where(Limit_display.id == limit_display_id)
    results = await session.exec(statement)
    limit_display = results.one()
    await session.delete(limit_display)
    await session.commit()
    return {"deleted": limit_display}
