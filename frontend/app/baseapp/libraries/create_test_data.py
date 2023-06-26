import plotly.graph_objects as go
import pandas as pd
import sys
from io import StringIO
from sqlalchemy import text


from sqlalchemy import create_engine
import pandas as pd
from dash import dash_table

import os
from os import environ, path

from dotenv import load_dotenv

load_dotenv(".env")

import mariadb
import pymysql

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
#MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_DATABASE = "data"
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

#MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/" + MARIADB_DATABASE

MARIADB_URI = "mariadb+pymysql://" + MARIADB_USERNAME + ":" + MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/" + MARIADB_DATABASE

#import psycopg2
engine = create_engine(MARIADB_URI)

print('##################### creating test data #####################')

## Limit Types

df = pd.DataFrame({
    'variable' : ['official','official'],
    'label' : ['All','Official'],
    'value' : ['0', '1'],
    'data_type' : ['boolean', 'boolean'],
    })

df.index.name='id'

#print(df)

with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='replace', index_label='id')

with engine.connect() as con:
    
    query = 'alter table data.dropdown_valuepairs drop id;'
    con.execute(text(query))
    #con.execute('alter table data.meta_valuepair add id serial primary key')
    query ='ALTER TABLE data.dropdown_valuepairs ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;'
    con.execute(text(query))
    
    
    
#df.to_sql('dropdown_valuepairs', con=engine, schema='data', if_exists='replace')

## Years

range_values = list(range(2000,2030))
variable_type = 'year'
data_type = 'number'
dropdown_values = []
for l in range_values:
    dropdown_values.append([variable_type,str(l),str(l),data_type])
df = pd.DataFrame(data=dropdown_values, columns=['variable','label','value','data_type'])

with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='append', index=False)

## Result Type

df = pd.DataFrame({
    'variable' : ['result_type','result_type', 'result_type'],
    'label' : ['Theory', 'Project', 'Experiment'],
    'value' : ['Th', 'Proj', 'Exp'],
    'data_type' : ['text', 'text','text']})

with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='append', index=False)
    
## Spin Dependence

df = pd.DataFrame({
    'variable' : ['spin_dependency','spin_dependency','spin_dependency'],
    'label' : ['All', 'spin-dependent', 'spin-independent'],
    'value' : ['All', 'SD', 'SI'],
    'data_type' : ['text', 'text','text']
})

with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='append', index=False)

## Greatest Hits

df = pd.DataFrame({
    'variable' : ['greatest_hit','greatest_hit'],
    'label' : ['All', 'Yes'],
    'value' : ['0', '1'],
    'data_type' : ['boolean','boolean']
})

with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='append', index=False)

## Experiments
'''
df = pd.DataFrame({
    'variable' : ['experiment','experiment', 'experiment', 'experiment', 'experiment','experiment','experiment'],
    'label' : ['All', 'Experiment DMTOOL', 'Experiment D',\
               'Experiment M', 'Experiment T', 'Experiment O', 'Experiment L'],
    'value' : ['All', 'Experiment DMTOOL', 'Experiment D',\
               'Experiment M', 'Experiment T', 'Experiment O', 'Experiment L'],
    'data_type' : ['text', 'text','text','text', 'text','text','text']
})
'''

experiments_list = [
"CDMS I (SUF)","CDMS II (Soudan)","SuperCDMS","LUX","XENON10",
"XENON100","XENON1T","ZEPLIN I","ZEPLIN II","ZEPLIN III","ZEPLIN IV",
"COSME","CUORICINO","DAMA","KIMS DMRC","ELEGANT V","Edelweiss",
"GEDEON","Genius","Genino","Heidelberg","IGEX","KIMS","MIBETA",
"Modane NaI","NAIAD","PICASSO","ROSEBUD","SIMPLE","Saclay",
"SuperK","TOKYO","UKDMC","WARP","Theory","Heidelberg-Moscow",
"Cuore","DAMA Xe","TEXONO","XMASS","IceCube","DMTPC","DEAP CLEAN",
"DAMA/LIBRA","CoGeNT","COUPP","LUX-ZEPLIN","Fermi","DarkSide","DAMIC",
"EURECA","DEAP-3600","PICO","PandaX","LHC","DRIFT","GAMBIT",
"CDEX-10","NEWS-G","XENONnT","CRESST"
]

experiment_list_length = len(experiments_list)
variable_list = ['experiment'] * experiment_list_length
data_type_list = ['text'] * experiment_list_length

df = pd.DataFrame({
    'variable' : variable_list,
    'label' : experiments_list,
    'value' : experiments_list,
    'data_type' : data_type_list
})


with engine.begin() as connection:
    df.to_sql(name='dropdown_valuepairs', con=connection,schema='data', if_exists='append', index=False)


#all_dropdown_pairs = pd.read_sql('SELECT variable,label, value FROM dropdown_valuepairs', con=engine)

#year_dropdown_pairs = all_dropdown_pairs[all_dropdown_pairs['variable']=='year']
#year_dropdown_pairs

all_dropdown_pairs = pd.read_sql('SELECT variable,label, value,data_type FROM dropdown_valuepairs', con=engine)
experiments_df = all_dropdown_pairs[all_dropdown_pairs['variable']=='experiment'].copy()
result_types_df  = all_dropdown_pairs[all_dropdown_pairs['variable']=='result_type'].copy()
spin_dependency_df  = all_dropdown_pairs[all_dropdown_pairs['variable']=='spin_dependence'].copy()
greatest_hit_df = all_dropdown_pairs[all_dropdown_pairs['variable']=='greatest_hits'].copy()
limit_types_df = all_dropdown_pairs[all_dropdown_pairs['variable']=='limit_type'].copy()
years_df = all_dropdown_pairs[all_dropdown_pairs['variable']=='year'].copy()

all_dropdown_pairs.head()

#years_df.to_dict('records')

filter_df = pd.DataFrame([[1,2]], columns=['variable','value'])
#add_this = pd.DataFrame
#filter_df


'''    
list = ['abc','def','hig']
df=pd.DataFrame(list)
df.columns=['names']
    
for s in selected_years_list:
    append_this = pd.DataFrame(['year', s],columns=['variable','value'])
    #print(append_this)
    filter_df = pd.concat([filter_df, append_this])
    


with engine.begin() as connection:
    df1 = pd.DataFrame({'name' : ['User 4', 'User 5']})
    df1.to_sql('users', con=connection, if_exists='append')
'''

from app.baseapp.libraries import letterxy as lxy

dmt = lxy.DMTool()
'''
with engine.begin() as connection:
    dmt = lxy.DMTool()
    dmdf = dmt.dmtdf
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    df_data = [1,'', 'Personal', '', '', 'GeV', 'cm^2', '1', '1', 'Black', 'Line',
           '', '', '', '', '', '', '', '', 0, '', 0, 0, '', 0, '', '', '']
'''
limits_metadata_empty = pd.DataFrame(data=[],
                                  columns= ['limit_id',
                                            'spin_dependency',
                                            'result_type',
                                            'measurement_type',
                                            'nomhash',
                                            'x_units',
                                            'y_units',
                                            'x_rescale',
                                            'y_rescale',
                                            'default_color',
                                            'default_style',
                                            'data_label',
                                            'file_name',
                                            'data_comment',
                                            'data_reference',
                                            'created_at',
                                            'updated_at',
                                            'creator_id',
                                            'experiment',
                                            'rating',
                                            'date_of_announcement',
                                            'public', 
                                            'official',
                                            'date_official',
                                            'greatest_hit',
                                            'date_of_run_start', 
                                            'date_of_run_end',
                                            'year'])
                                            



limits_metadata_df = limits_metadata_empty.copy()

# insert updated records from 'records_updated' to 'records'
# engine.execute("delete from data.limits_data;")
#engine.execute("delete from data.limits_metadata;")
#engine.execute("delete from data.meta_valuepair;")

# # Experiment dmtool

dmt.MakeDMTool(1000,1)
dmdf = dmt.dmtdf
dmdf.head(5)
#limits_metadata_df
index_id = 1
limits_metadata_df.loc[index_id,'limit_id'] = 1000
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment DMTOOL'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2023' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment DMTOOL' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'dmtool' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'dmtool' ## 

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='replace', index_label='id')
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='replace', index_label='id')
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='replace', index_label='id')

with engine.connect() as con:
    
    #query ='ALTER TABLE data.dropdown_valuepairs MODIFY id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;'
    #con.execute(text(query))
    
    query='alter table data.limits_data drop id;'
    con.execute(text(query))
    #con.execute('alter table data.meta_valuepair add id serial primary key')
    query='ALTER TABLE data.limits_data ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;'
    con.execute(text(query))  
    
    query='alter table data.limits_metadata drop id;'
    con.execute(text(query))  
    #con.execute('alter table data.meta_valuepair add id serial primary key') 
    query='ALTER TABLE data.limits_metadata ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;'
    con.execute(text(query))    
    
    query='alter table data.meta_valuepair drop id;'
    con.execute(text(query))
    query='ALTER TABLE data.meta_valuepair ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;'
    #con.execute('alter table data.meta_valuepair add id serial primary key') 
    con.execute(text(query))
    
    
    
    
limits_metadata_df = limits_metadata_empty.copy()


# # Experiment D

dmdf = dmt.ddf
dmdf['limit_id'] = 10
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'd'

#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 10
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment D'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2023' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment D' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'd' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'd' ## 
#limits_metadata_df

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append',index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)

limits_metadata_df = limits_metadata_empty.copy()


# # Experiment M

dmdf = dmt.mdf
dmdf['limit_id'] = 11
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'm'
#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 11
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment M'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2020' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment M' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'm' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'm' ## 
#limits_metadata_df

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)
limits_metadata_df = limits_metadata_empty.copy()


# # Experiment T

dmdf = dmt.tdf
dmdf['limit_id'] = 12
dmdf['trace_id'] = 1
dmdf['trace_name'] = 't'
#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 12
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment T'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2020' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment T' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 't' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 't' ## 
#limits_metadata_df

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)
limits_metadata_df = limits_metadata_empty.copy()

# # Experiment O

dmdf = dmt.odf
dmdf['limit_id'] = 13
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'o'
#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 13
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment O'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2020' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment O' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'o' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'o' ## 
#limits_metadata_df

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)

limits_metadata_df = limits_metadata_empty.copy()


# # Experiment L

dmdf = dmt.ldf
dmdf['limit_id'] = 14
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'l'
#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 14
limits_metadata_df.loc[index_id,'x_rescale'] = '1'
limits_metadata_df.loc[index_id,'y_rescale'] = '1'
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SD' # SI
limits_metadata_df.loc[index_id,'official'] = '1'
limits_metadata_df.loc[index_id,'experiment'] = 'Experiment L'
limits_metadata_df.loc[index_id,'result_type'] = 'Th' ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = '2020' ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = '0' ## 1
limits_metadata_df.loc[index_id,'public'] = '1' ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'dotted' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment L' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'l' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'l' ## 
#limits_metadata_df

value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')

meta_valuepair_df = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)

with engine.begin() as connection:
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append',index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append',index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append',index=False)

limits_metadata_df = limits_metadata_empty.copy()



    
    
   







