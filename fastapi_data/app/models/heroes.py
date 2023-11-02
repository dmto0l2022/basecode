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

class TeamBase(SQLModel):
    name: str = Field(index=True)

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="team")

class TeamRead(TeamBase):
    id: int

class HeroBase(SQLModel):
    name: str = Field(index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional[Team] = Relationship(back_populates="heroes")

class HeroRead(HeroBase):
    id: int

class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []
