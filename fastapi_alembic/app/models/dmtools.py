from sqlmodel import SQLModel, Field
from typing import Optional

from datetime import datetime
from datetime import date

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
#Limit, LimitCreate
#Plot_ownership, Plot_ownershipCreate
#Plot, PlotCreate


### Experiments

class ExperimentBase(SQLModel):
    name: str

class Experiment(ExperimentBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class ExperimentCreate(ExperimentBase):
    pass

## Limit Display

#fields:
#    id
#    name
#    limit_id
#    plot_id
#    trace_id
#    symbol
#    symbol_color
#    line_style
#    line_color
#    fill_color
#    color
#    style
#    created_at
#    updated_at
#    ceased_at

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
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Limit_display(Limit_displayBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_displayCreate(Limit_displayBase):
    pass
        
# Limit Ownership
## Fields
# id
# user_id
# limit_id
# created_at
# updated_at
# ceased_at

class Limit_ownershipBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    limit_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Limit_ownership(Limit_ownershipBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_ownershipCreate(Limit_ownershipBase):
    pass

## Limit

## Fields
'''
id
spin_dependency 
result_type 
measurement_type 
nomhash 
x_units 
y_units 
x_rescale 
y_rescale 
default_color 
default_style 
data_values 
data_label 
file_name 
data_comment
data_reference
created_at
updated_at
ceased_at
creator_id
experiment
rating
date_of_announcement
public
official
date_official
greatest_hit
date_of_run_start
date_of_run_end
year
'''

class LimitBase(SQLModel):
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
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    creator_id : int = Field(default=None, nullable=False, primary_key=False)
    experiment :  str = Field(default=None)
    rating : int = Field(default=None, nullable=False, primary_key=False)
    date_of_announcement : date = Field(default=date.today(), nullable=False)
    public : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    official : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    date_official : datetime = Field(default=date.today(), nullable=False)
    greatest_hit : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    date_of_run_start : date = Field(default=date.today(), nullable=False)
    date_of_run_end : date = Field(default=date.today(), nullable=False)
    year : int = Field(default=None, nullable=False, primary_key=False)

class Limit(LimitBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class LimitCreate(LimitBase):
    pass
        
## Plot Ownership 
# Fields
'''
id
user_id
plot_id
created_at
updated_at
ceased_at
'''

class Plot_ownershipBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    plot_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)

class Plot_ownership(Plot_ownershipBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class Plot_ownershipCreate(Plot_ownershipBase):
    pass

## Plot
## Fields
'''
id
name
x_min
x_max
y_min
y_max
x_units
y_units
user_id
created_at
updated_at
ceased_at
plot_png
legend_png
plot_eps
legend_eps
no_id
'''

class PlotBase(SQLModel):
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
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    plot_png : str = Field(default=None)
    legend_png : str = Field(default=None)
    plot_eps : str = Field(default=None)
    legend_eps : str = Field(default=None)
    no_id : int = Field(default=None, nullable=False, primary_key=False)

class Plot(PlotBase, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    id: int = Field(default=None, nullable=False, primary_key=True)

class PlotCreate(PlotBase):
    pass
