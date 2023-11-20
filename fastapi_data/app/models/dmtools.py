from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import ForeignKeyConstraint
## https://github.com/tiangolo/sqlmodel/issues/222
from sqlmodel import SQLModel, Field, Relationship
## https://stackoverflow.com/questions/74273829/how-to-correctly-use-joins-with-sqlmodel
## https://docs.sqlalchemy.org/en/20/dialects/mysql.html

from datetime import datetime

datetime_origin_str = '01/01/1980 00:00:00'

datetime_origin = datetime.strptime(datetime_origin_str, '%m/%d/%Y %H:%M:%S')

from typing import Optional
from typing import List


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

class ExperimentUpdate(SQLModel):
    name : str = Field(default=None, nullable=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True)

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
    old_limit_display_id : Optional[int] = Field(default=None, nullable=True)
    name: Optional[str] = Field(default=None,nullable=True)
    trace_name: Optional[str] = Field(default=None, nullable=True)
    old_limit_id : Optional[int] = Field(default=None, nullable=True)
    limit_id : Optional[int] = Field(default=None, foreign_key='limit.id', nullable=True)
    old_plot_id : Optional[int] = Field(default=None, nullable=True)
    plot_id : Optional[int] = Field(default=None, foreign_key='plot.id', nullable=True)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    symbol : Optional[str] = Field(default=None, nullable=True)
    symbol_color :  Optional[str] = Field(default=None, nullable=True)
    line_style : Optional[str] = Field(default=None, nullable=True)
    line_color :  Optional[str] = Field(default=None, nullable=True)
    fill_color :  Optional[str] = Field(default=None, nullable=True)
    color :  Optional[str] = Field(default=None, nullable=True)
    old_color :  Optional[str] = Field(default=None, nullable=True)
    style :  Optional[str] = Field(default=None, nullable=True)
    old_style :  Optional[str] = Field(default=None, nullable=True)
    created_at :  Optional[datetime]  = Field(default=datetime.utcnow(), nullable=True)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True)
    ceased_at : datetime = Field(default=datetime_origin, nullable=True)


class Limit_display(Limit_displayBase, table=True):
    ##__tablename__= "limit_display"
    ##__table_args__=  ({'mysql_engine':'InnoDB'})
    ##__table_args__= (ForeignKeyConstraint(["limit_id"], ["limit.id"], name="fk_limit_display_id"),)
    id: int = Field(default=None, nullable=False, primary_key=True)


class Limit_displayCreate(Limit_displayBase):
    pass

class Limit_displayUpdate(SQLModel):
    name: Optional[str] = Field(default=None,nullable=True)
    trace_name: Optional[str] = Field(default=None, nullable=True)
    limit_id : Optional[int] = Field(default=None, foreign_key='limit.id', nullable=True)
    plot_id : Optional[int] = Field(default=None, foreign_key='plot.id', nullable=True)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    symbol : Optional[str] = Field(default=None, nullable=True)
    symbol_color :  Optional[str] = Field(default=None, nullable=True)
    line_style : Optional[str] = Field(default=None, nullable=True)
    line_color :  Optional[str] = Field(default=None, nullable=True)
    fill_color :  Optional[str] = Field(default=None, nullable=True)
    color :  Optional[str] = Field(default=None, nullable=True)
    style :  Optional[str] = Field(default=None, nullable=True)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True)

# Limit Ownership
## Fields
# id
# user_id
# limit_id
# created_at
# updated_at
# ceased_at

class Limit_ownershipBase(SQLModel):
    old_ownership_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    limit_id : Optional[int] = Field(default=None, foreign_key='limit.id', nullable=True)
    old_user_id : Optional[int] = Field(default=None, nullable=True)
    old_limit_id : Optional[int] = Field(default=None, nullable=True)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime_origin, nullable=False)
    
class Limit_ownership(Limit_ownershipBase, table=True):
    ##__tablename__= "limit_ownership"
    ##__table_args__= (ForeignKeyConstraint(["limit_id"], ["limit.id"], name="fk_limit_ownership_id"),)
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_ownershipCreate(Limit_ownershipBase):
    pass

class Limit_ownershipUpdate(SQLModel):
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    limit_id : Optional[int] = Field(default=None, foreign_key='limit.id', nullable=True)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False)

#class Limit_ownershipRead(Limit_ownershipBase):
#    ##limit: Optional[Limit] = None

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

###

class ListOfLimitIDs(SQLModel):
    limit_ids: List[int]

###

class LimitBase(SQLModel):
    old_limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    measurement_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    nomhash : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_rescale : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_rescale : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    default_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    default_style : Optional[str] = Field(default=None, nullable=True, primary_key=False) 
    data_values : Optional[str] = Field(sa_column=Column(LONGTEXT), default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    file_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)
    creator_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    rating : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    date_of_announcement : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    public : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    official : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    date_official : Optional[date] = Field(default=date.today(), nullable=True, primary_key=False)
    greatest_hit : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    date_of_run_start : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    date_of_run_end : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)

class Limit(LimitBase, table=True):
    ##__tablename__ = "limit"
    ##__table_args__ =  ({'mysql_engine':'InnoDB'})
    id: int = Field(default=None, nullable=False, primary_key=True)

class LimitCreate(LimitBase):
    pass


class LimitUpdate(SQLModel):
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    measurement_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    nomhash : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_rescale : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_rescale : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    default_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    default_style : Optional[str] = Field(default=None, nullable=True, primary_key=False) 
    data_values : Optional[str] = Field(sa_column=Column(LONGTEXT), default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    file_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    creator_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    rating : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    date_of_announcement : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    public : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    official : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    date_official : Optional[date] = Field(default=date.today(), nullable=True, primary_key=False)
    greatest_hit : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    date_of_run_start : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    date_of_run_end : Optional[date] = Field(default=datetime_origin, nullable=True, primary_key=False)
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)

class LimitSelect(SQLModel):
    old_limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    measurement_type : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    public : Optional[int] = Field(default=None, nullable=True, primary_key=False) ## boolean
    official : Optional[int] = Field(default=None, nullable=True, primary_key=False) ## boolean
    greatest_hit : Optional[int] = Field(default=None, nullable=True, primary_key=False) ## boolean
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)

#####

'''
 limit_list_df_out = limit_data_df_out[['limit_id','data_label','data_reference', 'data_comment','year','experiment','spin_dependency','result_type','official',
                                           'greatest_hit']].copy()
'''
class Data_aboutBase(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    official : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    greatest_hit : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

class Data_about(Data_aboutBase, table=True):
    ##__tablename__= "data_about"
    id: int = Field(default=None, nullable=False, primary_key=True)

class Data_aboutCreate(Data_aboutBase):
    pass

class Data_aboutUpdate(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_reference : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    data_comment : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    year : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    experiment :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    spin_dependency : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    result_type :  Optional[str] = Field(default=None, nullable=True, primary_key=False)
    official : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    greatest_hit : Optional[int] = Field(default=0, nullable=True, primary_key=False) ## boolean
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)


'''
trace_list_df_out = limit_data_df_out[['limit_id','data_label','trace_id','trace_name',
                                           'line_color','symbol_color','fill_color','line','symbol']]
'''

class Data_appearanceBase(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    line_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    symbol_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    fill_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    line : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    symbol : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

class Data_appearance(Data_appearanceBase, table=True):
    ##__tablename__= "data_appearance"
    id: int = Field(default=None, nullable=False, primary_key=True)

class Data_appearanceCreate(Data_appearanceBase):
    pass

class Data_appearanceUpdate(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    data_label : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    line_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    symbol_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    fill_color : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    line : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    symbol : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)

####

class Data_dataBase(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    y : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)

class Data_data(Data_dataBase, table=True):
    ##__tablename__= "data_data"
    id: int = Field(default=None, nullable=False, primary_key=True)

class Data_dataCreate(Data_dataBase):
    pass

class Data_dataUpdate(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    y : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)



#####

class Limit_dataBase(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    y : Optional[float] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)
    
class Limit_data(Limit_dataBase, table=True):
    ##__tablename__= "limit_data"
    id: int = Field(default=None, nullable=False, primary_key=True)

class Limit_dataCreate(Limit_dataBase):
    pass

class Limit_dataUpdate(SQLModel):
    limit_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    trace_name : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)


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
    old_plot_ownership_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    old_user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : int = Field(default=None, foreign_key='plot.id', nullable=True, primary_key=False)
    old_plot_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=False, primary_key=False)

class Plot_ownership(Plot_ownershipBase, table=True):
    ##__tablename__= "plot_ownership"
    ##__table_args__=  ({'mysql_engine':'InnoDB'})
    ##__table_args__= (ForeignKeyConstraint(["plot_id"], ["plot.id"], name="fk_plot_ownership_id"),)
    id: int = Field(default=None, nullable=False, primary_key=True)

class Plot_ownershipCreate(Plot_ownershipBase):
    pass

class Plot_ownershipUpdate(SQLModel):
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    plot_id : int = Field(default=None, foreign_key='plot.id', nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=False, primary_key=False)


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
    old_plot_id : Optional[int] = Field(default=None, nullable=True)
    name : Optional[str] = Field(default=None,nullable=True, primary_key=False) ## Unique??
    x_min : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_max : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_min : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_max : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    old_user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    created_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    ceased_at : Optional[datetime] = Field(default=datetime_origin, nullable=True, primary_key=False)
    plot_png : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    legend_png : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    plot_eps : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    legend_eps : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    no_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)

class Plot(PlotBase, table=True):
    ##__tablename__= "plot"
    __table_args__ = (UniqueConstraint("user_id", "name", name="Constraint : Unique user id and plot name"),{'mysql_engine':'InnoDB'},)
    id: int = Field(default=None, nullable=False, primary_key=True)

class PlotCreate(PlotBase):
    pass

class PlotUpdate(SQLModel):
    name : Optional[str] = Field(default=None,nullable=True, primary_key=False) ## Unique??
    x_min : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_max : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_min : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_max : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    x_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    y_units : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    user_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)
    updated_at : Optional[datetime] = Field(default=datetime.utcnow(), nullable=True, primary_key=False)
    plot_png : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    legend_png : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    plot_eps : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    legend_eps : Optional[str] = Field(default=None, nullable=True, primary_key=False)
    no_id : Optional[int] = Field(default=None, nullable=True, primary_key=False)

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
