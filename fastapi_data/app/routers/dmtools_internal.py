from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header, Query
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List, Optional

from db import get_session

from models.dmtools import Experiment, ExperimentCreate
from models.dmtools import Limit_display, Limit_displayCreate
from models.dmtools import Limit_ownership, Limit_ownershipCreate
from models.dmtools import Limit, LimitCreate, LimitSelect
from models.dmtools import ListOfLimitIDs
from models.dmtools import Plot_ownership, Plot_ownershipCreate
from models.dmtools import Plot, PlotCreate

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/internal/data/'


from typing import List
from typing import Annotated


# Experiment CRUD

@router.get(api_base_url + "experiment", response_model=list[Experiment])
async def get_experiment(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Experiment))
    experiments = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]


@router.post(api_base_url + "experiment")
async def add_experiment(experiment: ExperimentCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    experiment = Experiment(name=experiment.name)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment

@router.delete(api_base_url + "experiment/{experiment_id}")
async def delete_experiment(experiment_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.get(api_base_url + "limit_display", response_model=list[Limit_display])
async def get_limit_display(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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


@router.post(api_base_url + "limit_display")
async def add_limit_display(limit_display: Limit_displayCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.delete(api_base_url + "limit_display/{limit_display_id}")
async def delete_limit_display(limit_display_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.get(api_base_url + "limit_ownership", response_model=list[Limit_ownership])
async def get_limit_ownership(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_ownership, Limit).where(Limit_ownership.limit_id == Limit.id))
    limit_ownerships = result.scalars().all()
    return [Limit_ownership(id = limit_ownership.id,
                            user_id = limit_ownership.user_id,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            updated_at = limit_ownership.updated_at,
                            data_comment = limit_ownership.data_comment)
            for limit_ownership in limit_ownerships]


@router.post(api_base_url + "limit_ownership")
async def add_limit_ownership(limit_ownership: Limit_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    limit_ownership = Limit_ownership(user_id = dmtool_userid,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            updated_at = limit_ownership.updated_at)
    session.add(limit_ownership)
    await session.commit()
    await session.refresh(limit_ownership)
    return limit_ownership

@router.delete(api_base_url + "limit_ownership/{limit_ownership_id}")
async def delete_limit_ownership(limit_ownership_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Limit_ownership).where(Limit_ownership.id == limit_ownership_id).where(Limit_ownership.user_id == dmtool_userid)
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

## get list of limits
'''
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items
'''  
## ListOfLimitIDs

#ListOfLimitIDs

@router.post(api_base_url + "listoflimits_simple/")
async def read_items(q: ListOfLimitIDs):
    print(q.limit_ids)
    return q.limit_ids



@router.post(api_base_url + "listoflimits")
#@router.get(api_base_url + "limits", response_model=list[Limit])
async def get_list_of_limits(list_of_limits: ListOfLimitIDs, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    #query_items = {"q": list_of_limits_qry}
    #list_of_limit_ids = query_items["q"]
    length = len(list_of_limits.limit_ids)
                              
    print("list of limits >>>>>>>>>>>", length, list_of_limits.limit_ids)
    print("length of list of limits >>>>>>>>>>>", length)
                              
    result = await session.execute(select(Limit_ownership,Limit).join(Limit).where(Limit_ownership.user_id == dmtool_userid).where(Limit.id.in_(list_of_limits.limit_ids)))
    
                              
    owneroflimits = result.all()
    print("owneroflimits >>>>>>>>>>>", owneroflimits)
    return_dict = dict()
    return_list = {'limits': []}
    #data = {'list': [{'a':'1'}]}
    #data['limits'].append({'b':'2'})
    #data
    #{'list': [{'a': '1'}, {'b': '2'}]}
    limit_count = 0
    for ool in owneroflimits:
        #just_owner = ool[0]
        just_limit = ool[1]
        append_this = {"id" :  just_limit.id,
                "old_limit_id" :  just_limit.old_limit_id,
                "spin_dependency" : just_limit.spin_dependency,
                "result_type" : just_limit.result_type,
                "measurement_type" : just_limit.measurement_type,
                "nomhash" : just_limit.nomhash,
                "x_units" : just_limit.x_units,
                "y_units" : just_limit.y_units,
                "x_rescale" : just_limit.x_rescale,
                "y_rescale" : just_limit.y_rescale,
                "default_color" : just_limit.default_color,
                "default_style" : just_limit.default_style,
                "data_values" : just_limit.data_values,
                "data_label" : just_limit.data_label,
                "file_name" : just_limit.file_name,
                "data_comment" : just_limit.data_comment,
                "data_reference" : just_limit.data_reference,
                "created_at" : just_limit.created_at,
                "updated_at" : just_limit.updated_at,
                "creator_id" : just_limit.creator_id,
                "experiment" : just_limit.experiment,
                "rating" : just_limit.rating,
                "date_of_announcement" : just_limit.date_of_announcement,
                "public" : just_limit.public,
                "official" : just_limit.official,
                "date_official" : just_limit.date_official,
                "greatest_hit" : just_limit.greatest_hit,
                "date_of_run_start" : just_limit.date_of_run_start,
                "date_of_run_end" : just_limit.date_of_run_end,
                "year" : just_limit.year}
        
        #return_dict[limit_count] = append_this
        return_list['limits'].append(append_this)
        limit_count += 1
    return return_list


## get limits to select

@router.get(api_base_url + "limitstoselect")
async def get_limit(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_ownership,Limit).join(Limit).where(Limit_ownership.user_id == dmtool_userid))
    owneroflimits = result.all()
    print("owneroflimits >>>>>>>>>>>", owneroflimits)
    return_dict = dict()
    return_list = {'limits': []}
    #data = {'list': [{'a':'1'}]}
    #data['limits'].append({'b':'2'})
    #data
    #{'list': [{'a': '1'}, {'b': '2'}]}
    limit_count = 0
    for ool in owneroflimits:
        #just_owner = ool[0]
        just_limit = ool[1]
        append_this = {"id" :  just_limit.id,
                "spin_dependency" : just_limit.spin_dependency,
                "result_type" : just_limit.result_type,
                "measurement_type" : just_limit.measurement_type,
                "nomhash" : just_limit.nomhash,
                "data_label" : just_limit.data_label,
                "data_comment" : just_limit.data_comment,
                "data_reference" : just_limit.data_reference,
                "experiment" : just_limit.experiment,
                "public" : just_limit.public,
                "official" : just_limit.official,
                "greatest_hit" : just_limit.greatest_hit,
                "year" : just_limit.year}
        
        #return_dict[limit_count] = append_this
        return_list['limits'].append(append_this)
        limit_count += 1
    return return_list


## get all limits

@router.get(api_base_url + "limits")
#@router.get(api_base_url + "limits", response_model=list[Limit])
async def get_limit(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_ownership,Limit).join(Limit).where(Limit_ownership.user_id == dmtool_userid))
    owneroflimits = result.all()
    print("owneroflimits >>>>>>>>>>>", owneroflimits)
    return_dict = dict()
    return_list = {'limits': []}
    #data = {'list': [{'a':'1'}]}
    #data['limits'].append({'b':'2'})
    #data
    #{'list': [{'a': '1'}, {'b': '2'}]}
    limit_count = 0
    for ool in owneroflimits:
        #just_owner = ool[0]
        just_limit = ool[1]
        append_this = {"id" :  just_limit.id,
                "old_limit_id" :  just_limit.old_limit_id,
                "spin_dependency" : just_limit.spin_dependency,
                "result_type" : just_limit.result_type,
                "measurement_type" : just_limit.measurement_type,
                "nomhash" : just_limit.nomhash,
                "x_units" : just_limit.x_units,
                "y_units" : just_limit.y_units,
                "x_rescale" : just_limit.x_rescale,
                "y_rescale" : just_limit.y_rescale,
                "default_color" : just_limit.default_color,
                "default_style" : just_limit.default_style,
                "data_values" : just_limit.data_values,
                "data_label" : just_limit.data_label,
                "file_name" : just_limit.file_name,
                "data_comment" : just_limit.data_comment,
                "data_reference" : just_limit.data_reference,
                "created_at" : just_limit.created_at,
                "updated_at" : just_limit.updated_at,
                "creator_id" : just_limit.creator_id,
                "experiment" : just_limit.experiment,
                "rating" : just_limit.rating,
                "date_of_announcement" : just_limit.date_of_announcement,
                "public" : just_limit.public,
                "official" : just_limit.official,
                "date_official" : just_limit.date_official,
                "greatest_hit" : just_limit.greatest_hit,
                "date_of_run_start" : just_limit.date_of_run_start,
                "date_of_run_end" : just_limit.date_of_run_end,
                "year" : just_limit.year}
        
        #return_dict[limit_count] = append_this
        return_list['limits'].append(append_this)
        limit_count += 1
    return return_list


## get one limit

@router.get(api_base_url + "limit/{limit_id}", response_model=Limit)
async def get_limit(limit_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(LimitOwnership,Limit).join(Limit).where(LimitOwnership.limit_id == limit_id).where(LimitOwnership.user_id == dmtool_userid)
    raw_data = await session.exec(statement)
    limits = raw_data.first()
    print("limit data >>>>>>>>>>>>>>>",  limits)
    limit_count = 0
    just_limit = limits[1]
    return just_limit

## add one limit

@router.post(api_base_url + "limit")
#@router.post(api_base_url + "limit")
async def add_limit(limit: LimitCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.delete(api_base_url + "limit/{limit_id}")
async def delete_limit(limit_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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


@router.get(api_base_url + "plot_ownership", response_model=list[Plot_ownership])
async def get_plot_ownership(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Plot_ownership))
    plot_ownerships = result.scalars().all()
    return [Plot_ownership(id = plot_ownership.id,
                            user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at
                         )
            for plot_ownership in plot_ownerships]


@router.post(api_base_url + "plot_ownership")
async def add_plot_ownership(plot_ownership: Plot_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    plot_ownership = Plot_ownership(user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at)
    session.add(plot_ownership)
    await session.commit()
    await session.refresh(plot_ownership)
    return plot_ownership

@router.delete(api_base_url + "plot_ownership/{plot_ownership_id}")
async def delete_plot_ownership(plot_ownership_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.get(api_base_url + "plot", response_model=list[Plot])
async def get_plot(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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


@router.post(api_base_url + "plot")
async def add_plot(plot: PlotCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
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

@router.delete(api_base_url + "plot/{plot_id}")
async def delete_plot_ownership(plot_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Plot).where(Plot.id == plot_id)
    results = await session.exec(statement)
    plot = results.one()
    await session.delete(plot)
    await session.commit()
    return {"deleted": plot}
