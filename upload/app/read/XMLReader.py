import os

import pandas as pd

from datetime import datetime

my_date = datetime.now()

print(my_date.isoformat())

2022-12-13T15:18:29.460762

data_id = "D" + my_date.strftime('%Y%m%d%H%M%S%f%z')

#data_id

dirname = os.getcwd()
print(dirname)

# Define scale factors [WT]

def get_scale_factor(unit):

    BARN_CM2= 1e-24
	if (unit == "b"):
		return BARN_CM

    elif (unit == "mb"):
		return 1e-3*BARN_CM2

    elif (unit == "ub"):
        return 1e-6*BARN_CM2

    elif (unit == "nb"):
        return 1e-9*BARN_CM2

    elif (unit == "pb"):
        return 1e-12*BARN_CM2

    elif (unit == "fb"):
        return 1e-15*BARN_CM2

    elif (unit == "ab"):
        return 1e-18*BARN_CM2

    elif (unit == "zb"):
        return 1e-21*BARN_CM2

    elif (unit == "yb"):
        return 1e-24*BARN_CM2

    else: 
        return 1

import xml.etree.ElementTree as ET
tree = ET.parse('example.xml')
root = tree.getroot()

#dv_find = root.findall('data-values')

#data = dv_find[0].text

def find_xml_text(root_in,tag_in):
    dv_find = root_in.findall(tag_in)
    return dv_find[0].text

data_values = find_xml_text(root,'data-values')
data_comment = find_xml_text(root,'data-comment')
data_label = find_xml_text(root,'data-label')
data_reference = find_xml_text(root,'data-reference')
date_of_announcement = find_xml_text(root,'date-of-announcement')
date_of_run_end = find_xml_text(root,'date-of-run-end')
date_of_run_start = find_xml_text(root,'date-of-run-start')
default_color = find_xml_text(root,'default-color')
default_style = find_xml_text(root,'default-style')
experiment = find_xml_text(root,'experiment')
public = find_xml_text(root,'public')
result_type = find_xml_text(root,'result-type')
spin_dependency = find_xml_text(root,'spin-dependency')
x_rescale = find_xml_text(root,'x-rescale')
x_units = find_xml_text(root,'x-units')
y_rescale = find_xml_text(root,'y-rescale')
y_units = find_xml_text(root,'y-units')
year = find_xml_text(root,'year')

data_record = [[data_values,data_comment,data_label,data_reference,date_of_announcement,date_of_run_end,
               date_of_run_start,default_color,default_style,experiment,
               public,result_type,spin_dependency,x_rescale,x_units,y_rescale,
               y_units,year
              ]]

rawdata_df = pd.DataFrame.from_records(data=data_record,\
                columns = ['data_values','data_comment','data_label','data_reference',\
                           'date_of_announcement','date_of_run_end','date_of_run_start',\
                           'default_color','default_style','experiment','public',\
                           'result_type','spin_dependency','x_rescale','x_units',\
                           'y_rescale','y_units','year'])

data_df = rawdata_df[['data_values']].copy()

metadata_df = rawdata_df[['data_comment','data_label','data_reference',\
                           'date_of_announcement','date_of_run_end','date_of_run_start',\
                           'default_color','default_style','experiment','public',\
                           'result_type','spin_dependency','x_rescale','x_units',\
                           'y_rescale','y_units','year']].copy()


#df.set_index('id', inplace=True, drop=False)

data_df.index.name = 'id'
data_df['id'] = data_df.index
data_df['data_id'] = data_id
metadata_df['data_id'] = data_id
#metadata_df['data_id'] = data_id
#data_df

data_string = data_df[['data_values']].iloc[0].values[0]
data_string = data_string.replace("{[", "")
data_string = data_string.replace("]}", "")

#row_in['id'].iloc[0]

lol = []

row_in = data_df

data_series = data_string.split("]")

#print(len(data_series))

for l in range(0,len(data_series)):
    #next_colour = next(palette)
    single_set = data_series[l]
    set_list = single_set.split(";")
    for i in set_list:
        z = i.split(" ");
        new_x = z[0].replace(",[", "")
        try:
            appendthis = [row_in['id'].iloc[0],row_in['data_id'].iloc[0],l,new_x,z[1]]
        except:
            appendthis = [row_in['id'].iloc[0],row_in['data_id'].iloc[0],l,0]

        lol.append(appendthis)

df_experiment = pd.DataFrame(data=lol,columns=['id','data_id','series','raw_x','raw_y'])

unit = "zb" # this will probably be provided by the user via a drop-down menu

scale_factor = float(get_scale_factor(unit))

df_experiment['x'] = df_experiment['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')

# add scale_factor here

df_experiment['y'] = df_experiment['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')#/scale_factor

#df_experiment['y'] =  df_experiment['y'].div(scale_factor).round(2)

df_experiment['scale_factor'] = scale_factor

df_experiment['scaled_y']=df_experiment[['y','scale_factor']].apply(pd.to_numeric,errors='coerce').fillna(0).eval('y/scale_factor')

#'experiment',

'''
def datastring2dataframe(row_in):

    #try:

    #data_list = row_in['data_values'].tolist()

    #data_list = row[['data_values']].iloc[0]

    #if isinstance(data_list, pd.DataFrame):

    #    row_data = next(data_list.iterrows())[1]

    #else:

    #    row_data = data_list

    data_string = row_in[['data_values']].iloc[0]

    data_string = data_string.replace("{[", "")

    data_string = data_string.replace("]}", "")

    x = data_string.split(";")

    lol = []

    

    

    data_series = data_string.split("]")

    #print(len(data_series))

    for l in range(0,len(data_series)):

        next_colour = next(palette)

        single_set = data_series[l]

        set_list = single_set.split(";")

        for i in set_list:

            z = i.split(" ");

            new_x = z[0].replace(",[", "")

            try:

                appendthis = [row_in['id'],row_in['data_label'],l,new_x,z[1],next_colour]

            except:

                appendthis = [row_in['id'],l,0,0]

            lol.append(appendthis)

    

    #for i in x:

    #    z = i.split(" ");

    #    appendthis = [z[0],z[1]]

    #    lol.append(appendthis)

    #lol

    df_experiment = pd.DataFrame(data=lol,columns=['id','data_label','series','raw_x','raw_y','suggested_color'])

    unit = "zb" # this will probably be provided by the user via a drop-down menu

    scale_factor = float(get_scale_factor(unit))

    df_experiment['x'] = df_experiment['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')

    # add scale_factor here

    df_experiment['y'] = df_experiment['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')#/scale_factor

    #df_experiment['y'] =  df_experiment['y'].div(scale_factor).round(2)

    df_experiment['scale_factor'] = scale_factor

    df_experiment['scaled_y']=df_experiment[['y','scale_factor']].apply(pd.to_numeric,errors='coerce').fillna(0).eval('y/scale_factor')

    #'experiment',

    #'series'

    

    #except:

    #    data_null = [[0,0]]

    #    df_experiment = pd.DataFrame(data=data_null,columns=['raw_x','raw_y'])#

    #    df_experiment['x'] = df_experiment['raw_x'].astype(str).astype(float)

    #    df_experiment['y'] = df_experiment['raw_y'].astype(str).astype(float)

    #df_experiment.dtypes

    return df_experiment

#row_in = data_df['data_values']

row_in = data_df

df_exp = datastring2dataframe(row_in)

'''

