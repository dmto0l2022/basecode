from typing import List, Optional, Annotated

import json

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, delete, join, update

from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header

from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from db import get_session

from models.heroes import Team, TeamCreate, Hero, HeroCreate, HeroUpdate, TeamMembers, TeamMemberAdd

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

api_base_url = '/dmtool/fastapi_data/test/example/'

@router.get(api_base_url + "teamwithheroes/{team_id}")
async def get_team_with_heroes(*, team_id: int, session: AsyncSession = Depends(get_session)):
    ##result = await session.execute(select(Team, Hero).join(Hero))
    #result_teamwithheroes = await session.execute(select(Hero, Team).where(Hero.team_id == Team.id))
    result_teamwithheroes = await session.execute(select(TeamMembers,Team,Hero).join(Team).join(Hero).where(TeamMembers.team_id == team_id))
    teamwithheroes = result_teamwithheroes.all()
    print("teamwithheroes >>>>>>>>>>>>>>>",type(teamwithheroes),  teamwithheroes)
    print("hero name  >>>>>>", teamwithheroes[0][1].name)
    return_dict = dict()
    hero_count = 0
    for twh in teamwithheroes:
        just_team = twh[1]
        just_hero = twh[2]
        append_this = {"team_name" : just_team.name, "team_id" : just_team.id, "hero_name" : just_hero.name}
        return_dict[hero_count] = append_this
        hero_count += 1
    #for jh in just_heros:
        
    #return_json = {"team_name" : just_team.name, "team_id" : just_team.id, "hero_id" : just_hero.id, "hero_name" : just_hero.name}
    #return_json = {"team_name" : just_team.name, "team_id" : just_team.id, "heroes" : just_heros}
    ## [(Hero(id=4, name='Hero 10', team_id=1), Team(id=1, name='Team 1'))]
    ## [(Team(id=1, name='Team 1'), Hero(id=4, name='Hero 10', team_id=1)), (Team(id=1, name='Team 1'), Hero(id=5, name='Hero 20', team_id=1))]
    ## [(TeamMembers(name='blah', id=2, team_id=3, hero_id=6), Team(id=3, name='Team 123'), Hero(id=6, name='Hero 123'))]
    ## SELECT hero.name, hero.team_id, hero.id, team.name AS name_1, team.id AS id_1 
    #resultDictionary = dict((x, y) for x, y in teamwithheroes[0])
    #return_json = json.dumps(return_dict, indent = 4) 
    return return_dict
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
    #hero = Hero(name=hero.name, team_id = hero.team_id)
    hero = Hero(name=hero.name)
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

@router.post(api_base_url + "teammember")
async def add_team_member(teammember: TeamMembers, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    teammember = TeamMembers(name=teammember.name, hero_id = teammember.hero_id, team_id = teammember.team_id )
    session.add(teammember)
    await session.commit()
    await session.refresh(teammember)
    return teammember

@router.delete(api_base_url + "team/{id}")
async def remove_team_team_member(teammember_id: int, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(TeamMembers).where(TeamMembers.id == teammember_id)
    results = await session.exec(statement)
    teammember = results.one()
    await session.delete(teammember)
    await session.commit()
    return {"deleted": teammember}


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


## update a hero record
''' example
@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.dict(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(db_hero, key, value)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

'''

@router.patch(api_base_url + "hero/{id}")
async def update_hero(hero_id: int,
                      record_in: HeroUpdate,
                      session: AsyncSession = Depends(get_session),
                      dmtool_userid: Annotated[int | None, Header()] = None):
    
    route_name = "Update Hero"
    record_in_data = record_in.dict(exclude_unset=True)
    get_records_statement = select(Hero).where(Hero.id == hero_id)
    record_update_statement = (update(Hero).where(Hero.id == hero_id).values(**record_in_data))
    
    db_records = await session.exec(get_records_statement)
    
    if not db_records:
        raise HTTPException(status_code=404, detail="Record not found - "+ route_name)
    
    #db_record_to_update = db_records.first()
    
    result = await session.execute(record_update_statement)
    await session.commit()
    
    updated_record = await session.exec(get_records_statement)
    return_record = updated_record.first()
    return {"updated": return_record}


## https://github.com/sqlalchemy/sqlalchemy/discussions/6630

'''

async def modify(
        self,
        db: AsyncSession,
        user_id: str,
        payload: Union[UserProfile, UserPersonProfile],
    ) -> UserProfileModel:
        """modify user profile partially"""

       # Normally when we try to update a row, we will find out if this row exists
        query = sa.select(UserProfileModel).where(UserProfileModel.id == user_id)
        result = await db.execute(query)
        profile = result.scalars().first()
        
        # if not, raise exception
        if not profile:
            raise HTTPException(400, detail=["profile not found"])
        
        # here is my question
        stmt = (
            sa.update(UserProfileModel)
            .where(UserProfileModel.id == user_id)
            .values(**payload.dict())
        )
        result = await db.execute(stmt)
        
        # why I don't need this?
        # db.refresh(profile)

        return profile
'''

