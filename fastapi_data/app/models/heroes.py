from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import ForeignKeyConstraint
## https://github.com/tiangolo/sqlmodel/issues/222
from sqlmodel import SQLModel, Field, Relationship
## https://stackoverflow.com/questions/74273829/how-to-correctly-use-joins-with-sqlmodel
## https://docs.sqlalchemy.org/en/20/dialects/mysql.html

from typing import Optional

from datetime import datetime
from datetime import date

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from models.base import Base
SQLModel.metadata = Base.metadata

from fastapi import FastAPI, Depends

## classes : Team, TeamRead, Hero, HeroRead, TeamReadWithHeroes

class TeamMemberBase(SQLModel):
    name: str = Field(index=True)

class TeamMembers(TeamMemberBase, table=True):
    __tablename__= "team_members"
    id: int = Field(default=None, primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id")
    hero_id: int = Field(default=None, foreign_key="hero.id")

class TeamMemberAdd(TeamMemberBase, table=False):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")

class TeamMembersRead(TeamMembers, table=False):
    pass
    
class TeamBase(SQLModel):
    name: str = Field(index=True)

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int

class HeroBase(SQLModel):
    name: str = Field(index=True)

class Hero(HeroBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class HeroRead(HeroBase):
    id: int

class HeroCreate(HeroBase):
    pass

'''
class ExperimentBase(SQLModel):
    old_experiment_id : Optional[int] = Field(default=None, nullable=True)
    name : str = Field(default=None, nullable=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True)

class Experiment(ExperimentBase, table=True):
    ##__tablename__= "experiment"
    ##__table_args__= ({'mysql_engine':'InnoDB'})
    id: int = Field(default=None, nullable=False, primary_key=True)

class ExperimentCreate(ExperimentBase):
    pass
'''
