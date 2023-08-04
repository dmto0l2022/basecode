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
    return [Limit_display(id = limit_display.id,
                        name = limit_display.name,
                        limit_id = limit_display.limit_id,
                        plot_id = limit_display.plot_id,
                        trace_id = limit_display.trace_id,
                        symbol = limit_display.symbol,
                        symbol_color = limit_display.symbol_color,
                        line_style = limit_display.line_style,
                        line_color = limit_display.line_color,
                        fill_color = limit_display.fill_color,
                        color = limit_display.color,
                        style = limit_display.style,
                        created_at = limit_display.created_at,
                        updated_at = limit_display.updated_at)
            for limit_display in limit_displays]


@router.post("/alembic/limit_display")
async def add_limit_display(limit_display: Limit_displayCreate, session: AsyncSession = Depends(get_session)):
    limit_display = Limit_display(name = limit_display.name,
                        limit_id = limit_display.limit_id,
                        plot_id = limit_display.plot_id,
                        trace_id = limit_display.trace_id,
                        symbol = limit_display.symbol,
                        symbol_color = limit_display.symbol_color,
                        line_style = limit_display.line_style,
                        line_color = limit_display.line_color,
                        fill_color = limit_display.fill_color,
                        color = limit_display.color,
                        style = limit_display.style,
                        created_at = limit_display.created_at,
                        updated_at = limit_display.updated_at)
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

# Limit_ownership CRUD
## Limit_ownership, Limit_ownershipCreate

'''
id
user_id
limit_id
created_at
updated_at

id = limit_ownership.id,
user_id = limit_ownership.user_id,
limit_id = limit_ownership.limit_id,
created_at = limit_ownership.created_at,
created_at = limit_ownership.created_at
'''

@router.get("/alembic/limit_ownership", response_model=list[Limit_ownership])
async def get_limit_ownership(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Limit_ownership))
    limit_ownerships = result.scalars().all()
    return [Limit_display(id = limit_ownership.id,
                            user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            created_at = limit_ownership.created_at)
            for limit_ownership in limit_ownerships]


@router.post("/alembic/limit_ownership")
async def add_limit_ownership(limit_ownership: Limit_ownershipCreate, session: AsyncSession = Depends(get_session)):
    limit_ownership = Limit_ownership(user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            created_at = limit_ownership.created_at)
    session.add(limit_ownership)
    await session.commit()
    await session.refresh(limit_ownership)
    return limit_ownership

@router.delete("/alembic/limit_ownership/{limit_ownership_id}")
async def delete_limit_ownership(limit_ownership_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Limit_ownership).where(Limit_ownership.id == limit_ownership_id)
    results = await session.exec(statement)
    limit_ownership = results.one()
    await session.delete(limit_ownership)
    await session.commit()
    return {"deleted": limit_ownership}

# Limit CRUD
# Limit, LimitCreate

'''
id
spin_dependency
result_type
measurement_type
nomhash
x_units 
y_units
x_rescale 
y_rescale 
default_color 
default_style 
data_values 
data_label 
file_name 
data_comment
data_reference
created_at
updated_at
creator_id
experiment
rating
date_of_announcement
public
official
date_official
greatest_hit
date_of_run_start
date_of_run_end
year
'''

@router.get("/alembic/limit", response_model=list[Limit])
async def get_limit(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Limit))
    limit = result.scalars().all()
    return [Limit(id = limit.id,
                spin_dependency = limit.spin_dependency,
                result_type = limit.result_type,
                measurement_type = limit.measurement_type,
                nomhash = limit.nomhash,
                x_units = limit.x_units,
                y_units = limit.y_units,
                x_rescale = limit.x_rescale,
                y_rescale = limit.y_rescale,
                default_color = limit.default_color,
                file_name  = limit.file_name,
                data_comment = limit.data_comment,
                data_reference = limit.data_reference,
                created_at = limit.created_at,
                updated_at = limit.updated_at,
                creator_id = limit.creator_id,
                experiment = limit.experiment,
                rating = limit.rating,
                date_of_announcement = limit.date_of_announcement,
                public = limit.public,
                official = limit.official,
                date_official = limit.date_official,
                greatest_hit = limit.greatest_hit,
                date_of_run_start = limit.date_of_run_start,
                date_of_run_end = limit.date_of_run_end,
                year = limit.year)
            for limit in limits]


@router.post("/alembic/limit")
async def add_limit(limit: LimitCreate, session: AsyncSession = Depends(get_session)):
    limit = Limit(spin_dependency = limit.spin_dependency,
                result_type = limit.result_type,
                measurement_type = limit.measurement_type,
                nomhash = limit.nomhash,
                x_units = limit.x_units,
                y_units = limit.y_units,
                x_rescale = limit.x_rescale,
                y_rescale = limit.y_rescale,
                default_color = limit.default_color,
                file_name  = limit.file_name,
                data_comment = limit.data_comment,
                data_reference = limit.data_reference,
                created_at = limit.created_at,
                updated_at = limit.updated_at,
                creator_id = limit.creator_id,
                experiment = limit.experiment,
                rating = limit.rating,
                date_of_announcement = limit.date_of_announcement,
                public = limit.public,
                official = limit.official,
                date_official = limit.date_official,
                greatest_hit = limit.greatest_hit,
                date_of_run_start = limit.date_of_run_start,
                date_of_run_end = limit.date_of_run_end,
                year = limit.year)
    session.add(limit)
    await session.commit()
    await session.refresh(limit)
    return limit

@router.delete("/alembic/limit/{limit_id}")
async def delete_limit(limit_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Limit).where(Limit.id == limit_id)
    results = await session.exec(statement)
    limit = results.one()
    await session.delete(limit)
    await session.commit()
    return {"deleted": limit}

# Plot_ownership
# Plot_ownership, Plot_ownershipCreate

'''
id
user_id
plot_id
created_at
updated_at
'''

@router.get("/alembic/plot_ownership", response_model=list[Limit_display])
async def get_plot_ownership(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Plot_ownership))
    plot_ownerships = result.scalars().all()
    return [Limit_display(id = limit_ownership.id,
                            user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            created_at = limit_ownership.created_at)
            for limit_ownership in limit_ownerships]


@router.post("/alembic/limit_ownership")
async def add_plot_ownership(limit_ownership: Limit_ownershipCreate, session: AsyncSession = Depends(get_session)):
    limit_ownership = Limit_ownership(user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            created_at = limit_ownership.created_at)
    session.add(limit_ownership)
    await session.commit()
    await session.refresh(limit_ownership)
    return limit_ownership

@router.delete("/alembic/limit_ownership/{limit_ownership_id}")
async def delete_plot_ownership(limit_ownership_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Limit_ownership).where(Limit_ownership.id == limit_ownership_id)
    results = await session.exec(statement)
    limit_ownership = results.one()
    await session.delete(limit_ownership)
    await session.commit()
    return {"deleted": limit_ownership}

# Plot CRUD
# Plot, PlotCreate

'''
id
name
x_min
x_max
y_min
y_max
x_units
y_units
user_id
created_at
updated_at
plot_png
legend_png
plot_eps
legend_eps
no_id
'''
