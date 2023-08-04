from sqlmodel import SQLModel, Field
from typing import Optional

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

# Declarative base object
#Base = declarative_base()
#SQLModel.metadata = Base.metadata

from models.base import Base
SQLModel.metadata = Base.metadata

## Classes

#Experiment, ExperimentCreate
#Limit_display, Limit_displayCreate
#Limit_ownership, Limit_ownershipCreate
#Limits, LimitsCreate
#Plot_ownership, Plot_ownershipCreate
#Plots, PlotsCreate


### Experiments

class ExperimentBase(SQLModel):
    name: str

class Experiment(ExperimentBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class ExperimentCreate(ExperimentBase):
    pass

## Limit Display

class Limit_displayBase(SQLModel):
    name: str = Field(default=None)
    limit_id : int = Field(default=None, nullable=False, primary_key=False)
    plot_id : int = Field(default=None, nullable=False, primary_key=False)
    trace_id : int = Field(default=None, nullable=False, primary_key=False)
    symbol : str = Field(default=None)
    symbol_color :  str = Field(default=None)
    line_style : str = Field(default=None)
    line_color :  str = Field(default=None)
    fill_color :  str = Field(default=None)
    color :  str = Field(default=None)
    style :  str = Field(default=None)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Limit_display(Limit_displayBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_displayCreate(Limit_displayBase):
    pass
        
## Limit Ownership

class Limit_ownershipBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    limit_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Limit_ownership(Limit_ownershipBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_ownershipCreate(Limit_ownershipBase):
    pass

## Limits

class LimitsBase(SQLModel):
    spin_dependency : str = Field(default=None)
    result_type : str = Field(default=None)
    measurement_type : str = Field(default=None)
    nomhash : str = Field(default=None)
    x_units : str = Field(default=None)
    y_units : str = Field(default=None)
    x_rescale : str = Field(default=None)
    y_rescale : str = Field(default=None)
    default_color : str = Field(default=None)
    default_style : str = Field(default=None) 
    data_values : str = Field(default=None)
    data_label : str = Field(default=None)
    file_name : str = Field(default=None)
    data_comment : str = Field(default=None)
    data_reference : str = Field(default=None)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    creator_id : int = Field(default=None, nullable=False, primary_key=False)
    experiment :  str = Field(default=None)
    rating : int = Field(default=None, nullable=False, primary_key=False)
    date_of_announcement : datetime = Field(default=datetime.utcnow(), nullable=False)
    public : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    official : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    date_official : datetime = Field(default=datetime.utcnow(), nullable=False)
    greatest_hit : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    date_of_run_start : datetime = Field(default=datetime.utcnow(), nullable=False)
    date_of_run_end : datetime = Field(default=datetime.utcnow(), nullable=False)
    year : int = Field(default=None, nullable=False, primary_key=False)

class Limits(LimitsBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class LimitsCreate(LimitsBase):
    pass
        
## Plot Ownership 

class Plot_ownershipBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    plot_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Plot_ownership(Plot_ownershipBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Plot_ownershipCreate(Plot_ownershipBase):
    pass

## Plots

class PlotsBase(SQLModel):
    name : str = Field(default=None,nullable=False, primary_key=False) ## Unique??
    x_min : str = Field(default=None)
    x_max : str = Field(default=None)
    y_min : str = Field(default=None)
    y_max : str = Field(default=None)
    x_units : str = Field(default=None)
    y_units : str = Field(default=None)
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    plot_png : str = Field(default=None)
    legend_png : str = Field(default=None)
    plot_eps : str = Field(default=None)
    legend_eps : str = Field(default=None)
    no_id : int = Field(default=None, nullable=False, primary_key=False)

class Plots(PlotsBase, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    id: int = Field(default=None, nullable=False, primary_key=True)

class PlotsCreate(PlotsBase):
    pass
