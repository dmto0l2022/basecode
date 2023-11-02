from typing import List, Optional

from fastapi import FastAPI, Depends
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

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
