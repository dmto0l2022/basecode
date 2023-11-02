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
    ##__tablename__= "experiment"
    __table_args__= ({'mysql_engine':'InnoDB'})
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
    ##__tablename__= "limit_display"
    __table_args__=  ({'mysql_engine':'InnoDB'})
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
    limit_id : int = Field(default=None, foreign_key='limit.id', nullable=True)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    
'''
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str

    role_id: Optional[int] = Field(
        default=None,
        foreign_key="user_role.role_id",
    )
    role: Optional["UserRole"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs=dict(lazy="selectin"),  # depends on your needs
    )

class UserRole(SQLModel, table=True):
    __tablename__ = "user_role"
    role_id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str

    users: list[User] = Relationship(back_populates="role")


'''


class Limit_ownership(Limit_ownershipBase, table=True):
    ##__tablename__= "limit_ownership"
    __table_args__= ({'mysql_engine':'InnoDB'}, ForeignKeyConstraint(["limit_id"], ["limit.id"], name="fk_limit_ownership_id"),)
    id: int = Field(default=None, nullable=False, primary_key=True)
    ##owned_limits: list["Limit"] = Relationship(back_populates="limit_ownership")

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
data_label __tablename__= "Exercise"
    __table_args__= {
        'mysql_engine':'InnoDB'
    }
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
    data_values : str = Field(sa_column=Column(LONGTEXT), default=None)
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
    date_official : date = Field(default=date.today(), nullable=False)
    greatest_hit : int = Field(default=None, nullable=False, primary_key=False) ## boolean
    date_of_run_start : date = Field(default=date.today(), nullable=False)
    date_of_run_end : date = Field(default=date.today(), nullable=False)
    year : int = Field(default=None, nullable=False, primary_key=False)
    ##ownership_id: int = Field(default=None, foreign_key='limit_ownership.id')
    
class Limit(LimitBase, table=True):
    ##__tablename__ = "limit"
    __table_args__ =  ({'mysql_engine':'InnoDB'})
    id: int = Field(default=None, nullable=False, primary_key=True)
    ##limit_ownership: Optional["Limit_ownership"] = Relationship(back_populates="owned_limits", sa_relationship_kwargs=dict(lazy="selectin"))

class LimitCreate(LimitBase):
    pass


'''
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str

    role_id: Optional[int] = Field(
        default=None,
        foreign_key="user_role.role_id",
    )
    role: Optional["UserRole"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs=dict(lazy="selectin"),  # depends on your needs
    )

class UserRole(SQLModel, table=True):
    __tablename__ = "user_role"
    role_id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str

'''
        
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
    ##__tablename__= "plot_ownership"
    __table_args__=  ({'mysql_engine':'InnoDB'})
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
    x_min : Optional[str] = Field(default=None)
    x_max : Optional[str] = Field(default=None)
    y_min : Optional[str] = Field(default=None)
    y_max : Optional[str] = Field(default=None)
    x_units : Optional[str] = Field(default=None)
    y_units : Optional[str] = Field(default=None)
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    plot_png : Optional[str] = Field(default=None)
    legend_png : Optional[str] = Field(default=None)
    plot_eps : Optional[str] = Field(default=None)
    legend_eps : Optional[str] = Field(default=None)
    no_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    ##ownership_id : int = Field(foreign_key="plot_ownership.id", nullable=True)
    
    ##plot_ownership: Optional[Plot_ownership] = Relationship(back_populates="PlotBase")

class Plot(PlotBase, table=True):
    ##__tablename__= "limit_ownership"
    __table_args__ = (UniqueConstraint("user_id", "name", name="Constraint : Unique user id and plot name"), {'mysql_engine':'InnoDB'})
    id: int = Field(default=None, nullable=False, primary_key=True)

class PlotCreate(PlotBase):
    pass

