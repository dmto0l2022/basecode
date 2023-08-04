from sqlmodel import SQLModel, Field
from typing import Optional

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String

# Declarative base object
#Base = declarative_base()
from models.base import Base
SQLModel.metadata = Base.metadata

# Classes

# Dropdown_valuepairs, Dropdown_valuepairsCreate

# Fields

#variable
#label
#value
#data_type

#name: str = Field(default=None)
#limit_id : int = Field(default=None, nullable=False, primary_key=False)
#symbol : str = Field(default=None)
#created_at : datetime = Field(default=datetime.utcnow(), nullable=False)

## dropdown_valuepair

class Dropdown_valuepairBase(SQLModel):
    variable : str = Field(default=None)
    label : str = Field(default=None)
    value : str = Field(default=None)
    data_type : str = Field(default=None)


class Dropdown_valuepair(Dropdown_valuepairBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class Dropdown_valuepairCreate(Dropdown_valuepairsBase):
    pass
