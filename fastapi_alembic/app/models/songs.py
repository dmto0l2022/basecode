from sqlmodel import SQLModel, Field
from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String

# Declarative base object
from models.base import Base
SQLModel.metadata = Base.metadata

class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass

### Tune

class TuneBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Tune(TuneBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class TuneCreate(TuneBase):
    pass

### Rate

class RateBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Rate(RateBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class RateCreate(RateBase):
    pass

## Experiment

class ExperimentBase(SQLModel):
    name: str

class Experiment(ExperimentBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class ExperimentCreate(ExperimentBase):
    pass
