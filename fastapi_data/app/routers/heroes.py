from typing import List, Optional, Annotated

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, delete

from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header

from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from db import get_session

from models.heroes import Team, TeamReadWithHeroes

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/test/example/'


'''
# Experiment CRUD

@router.get(api_base_url + "experiment", response_model=list[Experiment])
async def get_experiment(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Experiment))
    experiments = result.scalars().all()
    return [Experiment(name=experiment.name, id=experiment.id) for experiment in experiments]
'''


@app.get(api_base_url + "teams/", response_model=List[TeamReadWithHeroes])
async def get_teams(*, session: AsyncSession = Depends(get_session)) -> List[Team]:
    return session.exec(select(Team)).all()
