from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
import requests

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

from models.users import User_api_key

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/'


from typing import List
from typing import Annotated

'''
async def verify_api_token(dmtool_userid: str = Header(),  dmtool_apikey: str = Header(), session: AsyncSession = Depends(get_session)):
    print("hello from decorator")
    ## check api key existence
    #dmtool_user_int = int(dmtool_userid)
    statement = select(User_api_key).where(User_api_key.user_id == dmtool_userid).where(User_api_key.api_key == dmtool_apikey) ## and User_api_key.ceased_at==unceased_datetime_object)
    # print("statement >>>>>>>>>>>>>>>>" , str(statement))
    try:
        user_api_keys = await session.exec(statement)
        user_api_key = user_api_keys.one()
        return True
    except:
        raise HTTPException(status_code=400, detail="unauthorised request")
'''

async def verify_api_token(dmtool_userid: str = Header(),  dmtool_apikey: str = Header(), session: AsyncSession = Depends(get_session)):
    print("hello from decorator")
    url = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/checkapikey"
    headers={"dmtool-userid":dmtool_userid, "dmtool-apikey" : dmtool_apikey }
    r=requests.get(url, headers=headers)
    # print("statement >>>>>>>>>>>>>>>>" , str(statement))
    if r == 1:
        return True
    else:
        raise HTTPException(status_code=400, detail="unauthorised request")
        
    return r

# Experiment CRUD

@router.get(api_base_url + "experiment", response_model=list[Experiment], dependencies=[Depends(verify_api_token)])
async def get_experiment(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    result = await session.execute(select(Experiment))
    experiments = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]


@router.post(api_base_url + "experiment", dependencies=[Depends(verify_api_token)])
async def add_experiment(experiment: ExperimentCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    experiment = Experiment(name=experiment.name)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment

@router.delete(api_base_url + "experiment/{experiment_id}", dependencies=[Depends(verify_api_token)])
async def delete_experiment(experiment_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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

@router.get(api_base_url + "limit_display", response_model=list[Limit_display], dependencies=[Depends(verify_api_token)])
async def get_limit_display(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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


@router.post(api_base_url + "limit_display", dependencies=[Depends(verify_api_token)])
async def add_limit_display(limit_display: Limit_displayCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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

@router.delete(api_base_url + "limit_display/{limit_display_id}", dependencies=[Depends(verify_api_token)])
async def delete_limit_display(limit_display_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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
updated_at = limit_ownership.created_at
'''

@router.get(api_base_url + "limit_ownership", response_model=list[Limit_ownership], dependencies=[Depends(verify_api_token)])
async def get_limit_ownership(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    result = await session.execute(select(Limit_ownership))
    limit_ownerships = result.scalars().all()
    return [Limit_display(id = limit_ownership.id,
                            user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            updated_at = limit_ownership.updated_at)
            for limit_ownership in limit_ownerships]


@router.post(api_base_url + "limit_ownership", dependencies=[Depends(verify_api_token)])
async def add_limit_ownership(limit_ownership: Limit_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    limit_ownership = Limit_ownership(user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            updated_at = limit_ownership.updated_at)
    session.add(limit_ownership)
    await session.commit()
    await session.refresh(limit_ownership)
    return limit_ownership

@router.delete(api_base_url + "limit_ownership/{limit_ownership_id}", dependencies=[Depends(verify_api_token)])
async def delete_limit_ownership(limit_ownership_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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

## get all limits

@router.get(api_base_url + "limits", response_model=list[Limit], dependencies=[Depends(verify_api_token)])
async def get_limit(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    result = await session.execute(select(Limit))
    limits = result.scalars().all()
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
                default_style = limit.default_style,
                data_values = limit.data_values,
                data_label = limit.data_label,
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


## get one limit

@router.get(api_base_url + "limit/{limit_id}", response_model=Limit, dependencies=[Depends(verify_api_token)])
async def get_limit(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    statement = select(Limit).where(Limit.id == limit_id)
    limit = await session.exec(statement)
    return limit

## add one limit

@router.post(api_base_url + "limit", dependencies=[Depends(verify_api_token)])
async def add_limit(limit: LimitCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    limit = Limit(spin_dependency = limit.spin_dependency,
                result_type = limit.result_type,
                measurement_type = limit.measurement_type,
                nomhash = limit.nomhash,
                x_units = limit.x_units,
                y_units = limit.y_units,
                x_rescale = limit.x_rescale,
                y_rescale = limit.y_rescale,
                default_color = limit.default_color,
                default_style = limit.default_style,
                data_values = limit.data_values,
                data_label = limit.data_label,
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

@router.delete(api_base_url + "limit/{limit_id}", dependencies=[Depends(verify_api_token)])
async def delete_limit(limit_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
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


@router.get(api_base_url + "plot_ownership", response_model=list[Plot_ownership], dependencies=[Depends(verify_api_token)])
async def get_plot_ownership(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    result = await session.execute(select(Plot_ownership))
    plot_ownerships = result.scalars().all()
    return [Plot_ownership(id = plot_ownership.id,
                            user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at
                         )
            for plot_ownership in plot_ownerships]


@router.post(api_base_url + "plot_ownership", dependencies=[Depends(verify_api_token)])
async def add_plot_ownership(plot_ownership: Plot_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    plot_ownership = Plot_ownership(user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at)
    session.add(plot_ownership)
    await session.commit()
    await session.refresh(plot_ownership)
    return plot_ownership

@router.delete(api_base_url + "plot_ownership/{plot_ownership_id}", dependencies=[Depends(verify_api_token)])
async def delete_plot_ownership(plot_ownership_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    statement = select(Plot_ownership).where(Plot_ownership.id == plot_ownership_id)
    results = await session.exec(statement)
    plot_ownership = results.one()
    await session.delete(plot_ownership)
    await session.commit()
    return {"deleted": plot_ownership}

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

@router.get(api_base_url + "plot", response_model=list[Plot], dependencies=[Depends(verify_api_token)])
async def get_plot(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    result = await session.execute(select(Plot))
    plots = result.scalars().all()
    return [Plot(id = plot.id,
                    name = plot.name,
                    x_min = plot.x_min,
                    x_max = plot.x_max,
                    y_min = plot.y_min,
                    y_max = plot.y_max,
                    x_units = plot.x_units,
                    y_units = plot.y_units,
                    user_id = plot.user_id,
                    created_at = plot.created_at,
                    updated_at = plot.updated_at,
                    plot_png = plot.plot_png,
                    legend_png = plot.legend_png,
                    plot_eps = plot.plot_eps,
                    legend_eps = plot.legend_eps,
                    no_id = plot.no_id
                         )
            for plot in plots]


@router.post(api_base_url + "plot", dependencies=[Depends(verify_api_token)])
async def add_plot(plot: PlotCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    plot = Plot(name = plot.name,
                        x_min = plot.x_min,
                        x_max = plot.x_max,
                        y_min = plot.y_min,
                        y_max = plot.y_max,
                        x_units = plot.x_units,
                        y_units = plot.y_units,
                        user_id = plot.user_id,
                        created_at = plot.created_at,
                        updated_at = plot.updated_at,
                        plot_png = plot.plot_png,
                        legend_png = plot.legend_png,
                        plot_eps = plot.plot_eps,
                        legend_eps = plot.legend_eps,
                        no_id = plot.no_id)
    session.add(plot)
    await session.commit()
    await session.refresh(plot)
    return plot

@router.delete(api_base_url + "plot/{plot_id}", dependencies=[Depends(verify_api_token)])
async def delete_plot_ownership(plot_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None,
                            dmtool_apikey: Annotated[str | None, Header()] = None):
    statement = select(Plot).where(Plot.id == plot_id)
    results = await session.exec(statement)
    plot = results.one()
    await session.delete(plot)
    await session.commit()
    return {"deleted": plot}
