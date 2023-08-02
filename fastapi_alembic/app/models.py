from sqlmodel import SQLModel, Field
from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String

# Declarative base object
Base = declarative_base()
SQLModel.metadata = Base.metadata

class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
     __tablename__ = "tbl_song"
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass
