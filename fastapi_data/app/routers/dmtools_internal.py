from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header, Query
from sqlmodel import select, delete, update
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List, Optional

from db import get_session

from models.dmtools import Experiment, ExperimentCreate, ExperimentUpdate
from models.dmtools import Limit_display, Limit_displayCreate, Limit_displayUpdate
from models.dmtools import Limit_ownership, Limit_ownershipCreate, Limit_ownershipUpdate
from models.dmtools import Limit, LimitCreate, LimitUpdate,  LimitSelect
from models.dmtools import Limit_data, Limit_dataCreate, Limit_dataUpdate
from models.dmtools import Data_about, Data_aboutCreate, Data_aboutUpdate, Data_aboutDelete
from models.dmtools import Data_appearance, Data_appearanceCreate, Data_appearanceUpdate
from models.dmtools import Data_data, Data_dataCreate, Data_dataUpdate
from models.dmtools import ListOfLimitIDs
from models.dmtools import Plot_ownership, Plot_ownershipCreate, Plot_ownershipUpdate
from models.dmtools import Plot, PlotCreate, PlotUpdate

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/internal/data/'


from typing import List
from typing import Annotated


# Experiment CRUD

@router.post(api_base_url + "experiment")
async def create_experiment(experiment: ExperimentCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    experiment = Experiment(name=experiment.name)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment


@router.get(api_base_url + "experiments", response_model=list[Experiment])
async def read_experiments(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Experiment))
    experiments = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]

@router.get(api_base_url + "experiment")
async def read_experiment(experiment_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Experiment).where(Experiment.id == experiment_id))
    #experiments = result.scalars().all()
    #records = await session.exec(get_records_statement)
    return_record = result.first()
    print("return_record >>>>>>>>>", return_record)
    return return_record


@router.patch(api_base_url + "experiment/{experiment_id}")
async def update_experiment(experiment_id: int,
                      record_in: ExperimentUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Experiment"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Experiment).where(Experiment.id == experiment_id)
    record_update_statement = (update(Experiment).where(Experiment.id == experiment_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


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

@router.post(api_base_url + "limit_display", include_in_schema=False)
async def create_limit_display(limit_display: Limit_displayCreate, session: AsyncSession = Depends(get_session),
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

@router.get(api_base_url + "limit_displays", response_model=list[Limit_display], include_in_schema=False)
async def read_limit_displays(session: AsyncSession = Depends(get_session),
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

###
@router.get(api_base_url + "limit_display", include_in_schema=False)
async def read_limit_display(limit_display_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_display).where(Limit_display.id == limit_display_id))
    return_record = result.first()
    print("return_record >>>>>>>>>", return_record)
    return return_record

###


@router.patch(api_base_url + "limit_display/{id}", include_in_schema=False)
async def update_limit_display(limit_display_id: int,
                      record_in: Limit_displayUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Limit_display"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Limit_display).where(Limit_display.id == limit_display_id)
    record_update_statement = (update(Limit_display).where(Limit_display.id == limit_display_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}

@router.delete(api_base_url + "limit_display/{limit_display_id}", include_in_schema=False)
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

@router.post(api_base_url + "limit_ownership")
async def create_limit_ownership(limit_ownership: Limit_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    limit_ownership = Limit_ownership(user_id = dmtool_userid,
                            limit_id = limit_ownership.limit_id,
                            created_at = limit_ownership.created_at,
                            updated_at = limit_ownership.updated_at)
    session.add(limit_ownership)
    await session.commit()
    await session.refresh(limit_ownership)
    return limit_ownership

@router.get(api_base_url + "limit_ownerships", response_model=list[Limit_ownership])
async def read_limit_ownerships(session: AsyncSession = Depends(get_session),
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

###

@router.get(api_base_url + "limit_ownership")
async def read_limit_ownership(limit_ownership_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_ownership).where(Limit_ownership.id == limit_ownership_id))
    return_record = result.first()
    #print("return_record >>>>>>>>>", return_record)
    return return_record

###


@router.patch(api_base_url + "limit_ownership/{id}")
async def update_limit_ownership(limit_ownership_id: int,
                      record_in: Limit_ownershipUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Limit_ownership"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Limit_ownership).where(Limit_ownership.id == limit_ownership_id)
    record_update_statement = (update(Limit_ownership).where(Limit_ownership.id == limit_ownership_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


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
async def read_list_of_limits(list_of_limits: ListOfLimitIDs, session: AsyncSession = Depends(get_session),
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
async def read_limits(session: AsyncSession = Depends(get_session),
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

## add one limit

@router.post(api_base_url + "limit")
async def create_limit(limit: LimitCreate, session: AsyncSession = Depends(get_session),
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

## read one limit

@router.get(api_base_url + "limit/{limit_id}")
async def read_limit(limit_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Limit_ownership,Limit).join(Limit).where(Limit_ownership.limit_id == limit_id).where(Limit_ownership.user_id == dmtool_userid)
    raw_data = await session.exec(statement)
    limit = raw_data.first()
    #print("limit data >>>>>>>>>>>>>>>",  limits)
    #limit_count = 0
    return limit


@router.patch(api_base_url + "limit/{limit_id}")
async def update_limit(limit_id: int,
                      record_in: LimitUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Limit"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Limit).where(Limit.id == limit_id)
    record_update_statement = (update(Limit).where(Limit.id == limit_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


@router.delete(api_base_url + "limit/{limit_id}")
async def delete_limit(limit_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Limit).where(Limit.id == limit_id)
    results = await session.exec(statement)
    limit = results.one()
    await session.delete(limit)
    await session.commit()
    return {"deleted": limit}

#################


# Limit_data
# Limit_data, Limit_dataCreate

'''
id
limit_id
trace_id
trace_name
x
y
created_at
updated_at
'''

@router.post(api_base_url + "limit_data")
async def create_limit_data(limit_data_in: Limit_dataCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    limit_data = Limit_data(limit_id = limit_data_in.limit_id,
                            trace_id = limit_data_in.trace_id,
                            trace_name = limit_data_in.trace_name,
                            x = limit_data_in.x,
                            y = limit_data_in.x,
                            created_at = limit_data_in.created_at,
                            updated_at = limit_data_in.updated_at)
    session.add(limit_data)
    await session.commit()
    await session.refresh(limit_data)
    return limit_data

@router.post(api_base_url + "limit_dataset")
async def create_limit_dataset(limit_dataset_in: list[Limit_dataCreate], session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    counter = 0
    for ll in limit_dataset_in:
        limit_data = Limit_data(limit_id = ll.limit_id,
                                trace_id = ll.trace_id,
                                trace_name = ll.trace_name,
                                x = ll.x,
                                y = ll.y,
                                created_at = ll.created_at,
                                updated_at = ll.updated_at)
        session.add(limit_data)
        await session.commit()
        counter += 1
    return {'inserted' : counter}

@router.get(api_base_url + "limit_data_multiple", response_model=list[Limit_data])
async def read_limit_data_multiple(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Limit_data))
    limit_data_multiple = result.scalars().all()
    return [Limit_data(id = limit_data.id,
                            limit_id = limit_data.user_id,
                            trace_id = limit_data.plot_id,
                            trace_name = limit_data.plot_id,
                            x = limit_data.x,
                            y = limit_data.x,
                            created_at = limit_data.created_at,
                            updated_at = limit_data.updated_at
                         )
            for limit_data in limit_data_multiple]

###

@router.get(api_base_url + "limit_data_single_limit")
async def read_limit_data_single_limit(limit_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    results = await session.execute(select(Limit_data).where(Limit_data.limit_id == limit_id))
    #return_record = result.first()
    return_lol = []
    for l in results:
        append_this = l
        return_lol.append(append_this)
      
    print("return_lol >>>>>>>>>", return_lol)
    return return_lol

###
'''
@router.patch(api_base_url + "plot_ownership/{plot_ownership_id}")
async def update_plot_ownership(plot_ownership_id: int,
                      record_in: Plot_ownershipUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Plot_ownership"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Plot_ownership).where(Plot_ownership.id == plot_ownership_id)
    record_update_statement = (update(Plot_ownership).where(Plot_ownership.id == plot_ownership_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


@router.delete(api_base_url + "plot_ownership/{plot_ownership_id}")
async def delete_plot_ownership(plot_ownership_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Plot_ownership).where(Plot_ownership.id == plot_ownership_id)
    results = await session.exec(statement)
    plot_ownership = results.one()
    await session.delete(plot_ownership)
    await session.commit()
    return {"deleted": plot_ownership}

'''

################

# Plot_ownership
# Plot_ownership, Plot_ownershipCreate

'''
id
user_id
plot_id
created_at
updated_at
'''

@router.post(api_base_url + "plot_ownership")
async def create_plot_ownership(plot_ownership: Plot_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    plot_ownership = Plot_ownership(user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at)
    session.add(plot_ownership)
    await session.commit()
    await session.refresh(plot_ownership)
    return plot_ownership


@router.get(api_base_url + "plot_ownerships", response_model=list[Plot_ownership])
async def read_plot_ownerships(session: AsyncSession = Depends(get_session),
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

###

@router.get(api_base_url + "plot_ownership")
async def read_plot_ownership(plot_ownership_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Plot_ownership).where(Plot_ownership.id == plot_ownership_id))
    return_record = result.first()
    print("return_record >>>>>>>>>", return_record)
    return return_record

###

@router.patch(api_base_url + "plot_ownership/{plot_ownership_id}")
async def update_plot_ownership(plot_ownership_id: int,
                      record_in: Plot_ownershipUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Plot_ownership"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Plot_ownership).where(Plot_ownership.id == plot_ownership_id)
    record_update_statement = (update(Plot_ownership).where(Plot_ownership.id == plot_ownership_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


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
# Plot, PlotCreate, PlotUpdate

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

@router.post(api_base_url + "plot_ownership")
async def create_plot_ownership(plot_ownership: Plot_ownershipCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    plot_ownership = Plot_ownership(user_id = plot_ownership.user_id,
                            plot_id = plot_ownership.plot_id,
                            created_at = plot_ownership.created_at,
                            updated_at = plot_ownership.updated_at)
    session.add(plot_ownership)
    await session.commit()
    await session.refresh(plot_ownership)
    return plot_ownership

'''

@router.post(api_base_url + "plot")
async def create_plot(plot: PlotCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    plot = Plot(name = plot.name,
                        x_min = plot.x_min,
                        x_max = plot.x_max,
                        y_min = plot.y_min,
                        y_max = plot.y_max,
                        x_units = plot.x_units,
                        y_units = plot.y_units,
                        user_id = dmtool_userid,
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

@router.get(api_base_url + "plots", response_model=list[Plot])
async def read_plots(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    
    result = await session.execute(select(Plot_ownership,Plot).join(Plot).where(Plot_ownership.user_id == dmtool_userid))
                              
    #result = await session.execute(select(Plot))
    #plots = result.scalars().all()
    plots = result['Plot']
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


###

@router.get(api_base_url + "plot")
async def read_plot(plot_id: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Plot).where(Plot.id == plot_id))
    return_record = result.first()
    print("return_record >>>>>>>>>", return_record)
    return return_record


###

@router.patch(api_base_url + "plot/{plot_id}")
async def update_plot(plot_id: int,
                      record_in: PlotUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Plot"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Plot).where(Plot.id == plot_id)
    record_update_statement = (update(Plot).where(Plot.id == plot_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}

@router.delete(api_base_url + "plot/{plot_id}")
async def delete_plot(plot_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Plot).where(Plot.id == plot_id)
    results = await session.exec(statement)
    plot = results.one()
    await session.delete(plot)
    await session.commit()
    return {"deleted": plot}


### Data about

# Data_about, Data_aboutCreate, Data_aboutUpdate

'''
limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
     "x_units" : just_limit.x_units,
                "y_units" : just_limit.y_units,
                "x_rescale" : just_limit.x_rescale,
                "y_rescale" : just_limit.y_rescale,
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    official : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    greatest_hit : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

limit_id
data_label
data_reference
data_comment
year
experiment
spin_dependency
result_type
official
greatest_hit
created_at
updated_at

'''

@router.post(api_base_url + "data_about")
async def create_data_about(data_about_in: Data_aboutCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    data_about = Data_about(limit_id = data_about_in.limit_id,
                            plot_id = data_about_in.plot_id,
                            series_id = data_about_in.series_id,
                            data_label = data_about_in.data_label,
                            data_reference = data_about_in.data_reference,
                            data_comment = data_about_in.data_comment,
                            year = data_about_in.year,
                            experiment = data_about_in.experiment,
                            spin_dependency = data_about_in.spin_dependency,
                            result_type = data_about_in.result_type,
                            official = data_about_in.official,
                            greatest_hit = data_about_in.greatest_hit,
                            created_at = data_about_in.created_at,
                            updated_at = data_about_in.updated_at
                           )
    session.add(data_about)
    await session.commit()
    await session.refresh(data_about)
    return data_about


@router.get(api_base_url + "data_about")
async def read_data_about_for_plot(plot_id_in: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    results = await session.execute(select(Data_about).where(Data_about.plot_id == plot_id_in))
    #return_record = result.first()
    return_lol = []
    for l in results:
        append_this = l
        return_lol.append(append_this)
      
    print("return_lol >>>>>>>>>", return_lol)
    return return_lol


@router.patch(api_base_url + "data_about/{data_about_id}")
async def update_data_about(data_about_id: int,
                      record_in: Data_aboutUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Data_about"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Data_about).where(Data_about.id == data_about_id)
    record_update_statement = (update(Data_about).where(Data_about.id == data_about_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


@router.delete(api_base_url + "data_about")
async def delete_data_about(data_about_delete_in: Data_aboutDelete, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Data_about).where(Data_about.plot_id == data_about_delete_in.plot_id).where(Data_about.limit_id == data_about_delete_in.limit_id)
    results = await session.exec(statement)
    data_about = results.one()
    await session.delete(data_about)
    await session.commit()
    return {"deleted": data_about}



## Data appearance

# Limit_data
# Limit_data, Limit_dataCreate

'''
  limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
  data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
  trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  line_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  symbol_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  fill_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  line : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  symbol : Optional[str] = Field(default=None, nullable=True, primary_key=False)
  created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
  updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
  ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

  limit_id
  data_label
  trace_id
  trace_name
  line_color
  symbol_color
  fill_color
  line
  symbol
  created_at
  updated_at
  
'''

@router.post(api_base_url + "data_appearance")
async def create_data_appearance(data_appearance_in: Data_appearanceCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    data_appearance = Data_appearance(
                            limit_id = data_appearance_in.limit_id,
                            plot_id = data_appearance_in.plot_id,
                            series_id = data_appearance_in.series_id,
                            data_label = data_appearance_in.data_label,
                            x_units = data_appearance_in.x_units,
                            y_units = data_appearance_in.y_units,
                            x_rescale = data_appearance_in.x_rescale,
                            y_rescale = data_appearance_in.y_rescale,
                            trace_id = data_appearance_in.trace_id,
                            trace_name = data_appearance_in.trace_name,
                            line_color = data_appearance_in.line_color,
                            symbol_color = data_appearance_in.symbol_color,
                            fill_color = data_appearance_in.fill_color,
                            line = data_appearance_in.line,
                            symbol = data_appearance_in.symbol,
                            created_at = data_appearance_in.created_at,
                            updated_at = data_appearance_in.updated_at)
    session.add(data_appearance)
    await session.commit()
    await session.refresh(data_appearance)
    return data_appearance



@router.get(api_base_url + "data_appearance")
async def read_data_appearance_for_plot(plot_id_in: int,session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    results = await session.execute(select(Data_appearance).where(Data_appearance.plot_id == plot_id_in))
    #return_record = result.first()
    return_lol = []
    for l in results:
        append_this = l
        return_lol.append(append_this)
      
    print("return_lol >>>>>>>>>", return_lol)
    return return_lol


@router.patch(api_base_url + "data_appearance/{data_appearance_id}")
async def update_data_appearance(data_appearance_id: int,
                      record_in: Data_appearanceUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Data Appearance"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Data_appearance).where(Data_appearance.id == data_appearance_id)
    record_update_statement = (update(Data_appearance).where(Data_appearance.id == data_appearance_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


@router.delete(api_base_url + "data_appearance/{data_appearance_id}")
async def delete_data_appearance(data_appearance_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Data_appearance).where(Data_appearance.id == data_appearance_id)
    results = await session.exec(statement)
    data_appearance = results.one()
    await session.delete(data_appearance)
    await session.commit()
    return {"deleted": data_appearance}

## Data data

# Limit_data
# Limit_data, Limit_dataCreate

'''

   limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    y : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

id
limit_id
trace_id
trace_name
x
y
created_at
updated_at
'''

@router.post(api_base_url + "data_data")
async def create_data_datapoint(data_data_in: Data_dataCreate, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    data_data = Data_data(limit_id = data_data_in.limit_id,
                          plot_id = data_data_in.plot_id,
                          series_id = data_data_in.series_id,
                          trace_id = data_data_in.trace_id,
                          trace_name = data_data_in.trace_name,
                          x_units = data_data_in.x_units,
                          y_units = data_data_in.y_units,
                          x_rescale = data_data_in.x_rescale,
                          y_rescale = data_data_in.y_rescale,
                          x = data_data_in.x,
                          y = data_data_in.y,
                          created_at = data_data_in.created_at,
                          updated_at = data_data_in.updated_at)
    session.add(data_data)
    await session.commit()
    await session.refresh(data_data)
    return data_data

@router.post(api_base_url + "data_data_dataset")
async def create_data_dataset(data_data_dataset_in: list[Data_dataCreate], session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    counter = 0
    for ll in data_data_dataset_in:
        data_data = Data_data(limit_id = ll.limit_id,
                              plot_id = ll.plot_id,
                              series_id = ll.series_id,
                                trace_id = ll.trace_id,
                                trace_name = ll.trace_name,
                                x_units = ll.x_units,
                                y_units = ll.y_units,
                                x_rescale = ll.x_rescale,
                                y_rescale = ll.y_rescale,
                                x = ll.x,
                                y = ll.y,
                                created_at = ll.created_at,
                                updated_at = ll.updated_at)
        session.add(data_data)
        await session.commit()
        counter += 1
    return {'inserted' : counter}

@router.get(api_base_url + "data_dataset", response_model=list[Data_data])
async def read_data_dataset(limit_id_in: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Data_data).where(Data_data.limit_id == limit_id_in))
    data_data_dataset = result.scalars().all()
    return [Data_data(id = data_data.id,
                            limit_id = data_data.limit_id,
                            plot_id = data_data.plot_id,
                            series_id = data_data.series_id,
                            trace_id = data_data.trace_id,
                            trace_name = data_data.trace_name,
                            x_units = data_data.x_units,
                            y_units = data_data.y_units,
                            x_rescale = data_data.x_rescale,
                            y_rescale = data_data.y_rescale,
                            x = data_data.x,
                            y = data_data.x,
                            created_at = data_data.created_at,
                            updated_at = data_data.updated_at
                         )
            for data_data in data_data_dataset]


@router.patch(api_base_url + "data_data/{data_data_id}")
async def update_data_data(data_data_id: int,
                      record_in: Data_dataUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Data_data"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Data_data).where(Data_data.id == data_data_id)
    record_update_statement = (update(Data_data).where(Data_data.id == data_data_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


@router.delete(api_base_url + "data_data/{data_data_id}")
async def delete_data_data(data_data_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Data_data).where(Data_data.id == data_data_id)
    results = await session.exec(statement)
    data_data = results.one()
    await session.delete(data_data)
    await session.commit()
    return {"deleted": data_data}



