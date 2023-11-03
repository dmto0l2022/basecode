from typing import List, Optional, Annotated

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, delete, join

from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header

from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from db import get_session

from models.heroes import Team, TeamCreate, Hero, HeroCreate, TeamReadWithHeroes

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/test/example/'

@router.get(api_base_url + "teamwithheroes/") ##, response_model=list[TeamReadWithHeroes])
async def get_team_with_heroes(*, session: AsyncSession = Depends(get_session)) -> List[Team]:
    ##result = await session.execute(select(Team, Hero).join(Hero))
    result_teamwithheroes = await session.execute(select(Hero, Team).where(Hero.team_id == Team.id))
    teamwithheroes = result_teamwithheroes.all()
    print("teamwithheroes >>>>>>>>>>>>>>>",type(teamwithheroes),  teamwithheroes)
    print("hero name  >>>>>>", teamwithheroes[0][1].name)
    ## [(Hero(id=4, name='Hero 10', team_id=1), Team(id=1, name='Team 1'))]
    ## SELECT hero.name, hero.team_id, hero.id, team.name AS name_1, team.id AS id_1 
    #resultDictionary = dict((x, y) for x, y in teamwithheroes[0])
    return {"hero name" : teamwithheroes[0][1].name}
    ##[Team(name=team.hero_name, team_id=team.team_id, hero_id = team.hero_id, team_name= team.team_name ) for team in teamwithheroes]

'''
@router.get(api_base_url + "teamwithheroes/{team_id}", response_model=TeamReadWithHeroes)
async def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = await session.execute(select(Team, team_id))
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
'''
@router.get(api_base_url + "teams/", response_model=list[Team])
async def get_team(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Team))
    teams = result.scalars().all()
    return [Team(name=team.name, id=team.id) for team in teams]

@router.get(api_base_url + "heroes/", response_model=list[Hero])
async def get_heroes(session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(Hero))
    heroes = result.scalars().all()
    return [Hero(name=hero.name, id=hero.id) for hero in heroes]


@router.post(api_base_url + "hero")
async def add_hero(hero: Hero, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    hero = Hero(name=hero.name, team_id = hero.team_id)
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero

@router.post(api_base_url + "team")
async def add_team(team: Team, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    team = Team(name=team.name)
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team

@router.delete(api_base_url + "team/{id}")
async def delete_team(team_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Team).where(Team.id == team_id)
    results = await session.exec(statement)
    team = results.one()
    await session.delete(team)
    await session.commit()
    return {"deleted": team}

@router.delete(api_base_url + "hero/{id}")
async def delete_hero(hero_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(Hero).where(Hero.id == hero_id)
    results = await session.exec(statement)
    hero = results.one()
    await session.delete(hero)
    await session.commit()
    return {"deleted": hero}
