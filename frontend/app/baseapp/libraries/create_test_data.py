import plotly.graph_objects as go
import pandas as pd
import sys
from io import StringIO


from sqlalchemy import create_engine
import pandas as pd
from dash import dash_table

import os
from os import environ, path

from dotenv import load_dotenv

load_dotenv(".env")

import mariadb

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
#MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_DATABASE = "data"
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/" + MARIADB_DATABASE

#import psycopg2
engine = create_engine(MARIADB_URI)

## Limit Types

df = pd.DataFrame({
    'variable' : ['limit_type','limit_type'],
    'label' : ['All','Official'],
    'value' : ['-1', '1'],
    'data_type' : ['number', 'number'],
    })
df.to_sql('dropdown_valuepairs', con=engine, if_exists='replace')

## Years

range_values = list(range(2000,2024))
variable_type = 'year'
data_type = 'number'
dropdown_values = []
for l in range_values:
    dropdown_values.append([variable_type,str(l),str(l),data_type])
df = pd.DataFrame(data=dropdown_values, columns=['variable','label','value','data_type'])  
df.to_sql('dropdown_valuepairs', con=engine, if_exists='append')

## Result Type

df = pd.DataFrame({
    'variable' : ['result_type','result_type', 'result_type'],
    'label' : ['Theory', 'Project', 'Experiment'],
    'value' : ['Th', 'Proj', 'Exp'],
    'data_type' : ['text', 'text','text']})
df.to_sql('dropdown_valuepairs', con=engine, if_exists='append')

## Spin Dependence

df = pd.DataFrame({
    'variable' : ['spin_dependence','spin_dependence','spin_dependence'],
    'label' : ['All', 'spin-dependent', 'spin-independent'],
    'value' : ['All', 'SD', 'SI'],
    'data_type' : ['text', 'text','text']
})

df.to_sql('dropdown_valuepairs', con=engine, if_exists='append')

## Greatest Hits

df = pd.DataFrame({
    'variable' : ['greatest_hits','greatest_hits','greatest_hits'],
    'label' : ['All', 'No', 'Yes'],
    'value' : ['-1', '0', '1'],
    'data_type' : ['number', 'number','number']
})
df.to_sql('dropdown_valuepairs', con=engine, if_exists='append')

## Experiments

df = pd.DataFrame({
    'variable' : ['experiment','experiment', 'experiment', 'experiment', 'experiment','experiment','experiment'],
    'label' : ['All', 'Experiment DMTOOL', 'Experiment D',\
               'Experiment M', 'Experiment T', 'Experiment O', 'Experiment L'],
    'value' : ['All', 'Experiment DMTOOL', 'Experiment D',\
               'Experiment M', 'Experiment T', 'Experiment O', 'Experiment L'],
    'data_type' : ['text', 'text','text','text', 'text','text','text']
})
df.to_sql('dropdown_valuepairs', con=engine, if_exists='append')


all_dropdown_pairs = pd.read_sql('SELECT variable,label, value FROM dropdown_valuepairs', con=engine)

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
    '''


with engine.begin() as connection:
    df1 = pd.DataFrame({'name' : ['User 4', 'User 5']})
    df1.to_sql('users', con=connection, if_exists='append')

import letterxy as lxy

dmt = lxy.DMTool()

with engine.begin() as connection:
    dmt = lxy.DMTool()
    dmdf = dmt.dmtdf
    #dmdf.index.names = ['limit_id']
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    df_data = [1,'', 'Personal', '', '', 'GeV', 'cm^2', '1', '1', 'Black', 'Line',
           '', '', '', '', '', '', '', '', 0, '', 0, 0, '', 0, '', '', '']

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
engine.execute("delete from data.limits_data;")
engine.execute("delete from data.limits_metadata;")
engine.execute("delete from data.meta_valuepair;")

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
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)

limits_metadata_df = limits_metadata_empty.copy()


# # Experiment D

dmdf = dmt.ddf
dmdf['limit_id'] = 10
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'd'

#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 1000
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
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)

limits_metadata_df = limits_metadata_empty.copy()


# # Experiment M

dmdf = dmt.mdf
dmdf['limit_id'] = 11
dmdf['trace_id'] = 1
dmdf['trace_name'] = 'm'
#limits_metadata_df
index_id = 3
limits_metadata_df.loc[index_id,'limit_id'] = 1000
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
limits_metadata_df.loc[index_id,'limit_id'] = 1000
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
limits_metadata_df.loc[index_id,'limit_id'] = 1000
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
limits_metadata_df.loc[index_id,'limit_id'] = 1000
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
    dmdf.to_sql('limits_data', con=connection, if_exists='append', index=False)
    limits_metadata_df.to_sql('limits_metadata', con=connection, if_exists='append', index=False)
    meta_valuepair_df.to_sql('meta_valuepair', con=connection, if_exists='append', index=False)
limits_metadata_df = limits_metadata_empty.copy()


#fig = go.Figure(go.Scatter(x=[0,1,2,0,None,3,3,5,5,3], y=[0,2,0,0,None,0.5,1.5,1.5,0.5,0.5], fill="toself"))
#fig.show()


limits_metadata_df = limits_metadata_empty.copy()
index_id = 4
limits_metadata_df.loc[index_id,'limit_id'] = 14
limits_metadata_df.loc[index_id,'x_rescale'] = 1
limits_metadata_df.loc[index_id,'y_rescale'] = 1
limits_metadata_df.loc[index_id,'x_units'] = 'GeV'
limits_metadata_df.loc[index_id,'y_units'] =  'cm^2'
limits_metadata_df.loc[index_id,'spin_dependency'] = 'SI' # SD, SI
limits_metadata_df.loc[index_id,'official'] = 1
limits_metadata_df.loc[index_id,'experiment'] = "Experiment L"
limits_metadata_df.loc[index_id,'result_type'] = "Th" ## Proj, Exp
limits_metadata_df.loc[index_id,'year'] = "2023" ## Proj, Exp
limits_metadata_df.loc[index_id,'greatest_hit'] = 1 ## 0, 1
limits_metadata_df.loc[index_id,'public'] = 1 ## 0
limits_metadata_df.loc[index_id,'default_color'] = 'black' ## 0
limits_metadata_df.loc[index_id,'default_style'] = 'solid' ## 0
limits_metadata_df.loc[index_id,'data_comment'] = 'Experiment L' ## 0
limits_metadata_df.loc[index_id,'data_reference'] = 'l' ## 0
limits_metadata_df.loc[index_id,'data_label'] = 'l' ## 


value_var_list = list(limits_metadata_df.columns)
value_var_list.remove('limit_id')
value_var_list


meta_valuepair = pd.melt(limits_metadata_df, id_vars=['limit_id'], value_vars=value_var_list)


#meta_valuepair


thisdict ={
    "spin_dependency": "SI",
    "year": "2023",
}
thisdict

D_coords = [[25,0],[35,0],[65,5],[90,25],[100,50],[90,75],
            [65,95],[35,100],
            [60,85],[75,65],[80,50],
            [75,35],[60,15],[35,0],[35,100],[25,100],[25,0]]

df = pd.DataFrame(data=D_coords,columns=['x','y'])


def GetLimits(meta_valuepair_in, thisdict_in):
    meta_valuepair_working = meta_valuepair_in.copy()
    for key in thisdict_in:
        print(key, '->', thisdict_in[key])
        limits_found = 
        meta_valuepair_working['limit_id'][(meta_valuepair_working['value']==thisdict_in[key]) & (meta_valuepair_working['variable']==key)]
        print(list(limits_found))
        limits_found_list = list(limits_found)
        df_filter = meta_valuepair_working["limit_id"].isin(limits_found_list)
        #print(df_filter)
        meta_valuepair_working = meta_valuepair_working[df_filter]
        #print(meta_valuepair_working)

GetLimits(meta_valuepair,thisdict)   

MDATA = StringIO("""x,y
80,75
80,0
90,0
90,100
80,75
55,10
50,0
20,65
20,0
10,0
10,100
55,10""")
df = pd.read_csv(MDATA, sep=",")MDATA = StringIO("""x,y
80,75
90,100
90,0
80,0
80,75
55,15
50,0
20,75
20,0
10,0
10,100
20,100
55,15
""")
df = pd.read_csv(MDATA, sep=",")df# Create figure
fig = go.Figure()

fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    paper_bgcolor="LightSteelBlue",
)

plot_df = dmt.dmtdf

fig.update_layout(yaxis_range=[0,100])
fig.update_layout(xaxis_range=[0,600])

trace_letters = ['d','m','t','o1','o2','l']
# Loop df columns and plot columns to the figure
for i in trace_letters:
#    col_name = 'S'+ str(i)
    trace_df = plot_df[plot_df['letter']==i]
    fig.add_trace(go.Scatter(x=trace_df['x'], y=trace_df['y'],name=i,
                        mode='lines', # 'lines' or 'markers',
                         fill="toself"
                        ))
            


