import requests
import json
import pandas as pd

def parse_series_and_values(limits_dataframe_in):
    limit_data = []
    for index, row in limits_dataframe_in.iterrows():
        #print(row['id'], row['data_values'])
        data_label = row[['data_label']].iloc[0]
        data_string = row[['data_values']].iloc[0]
        data_string = data_string.replace("{[", "")
        data_string = data_string.replace("]}", "")
        #print(data_string)
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
                    appendthis = [row['id'],data_label,l,new_x,z[1],next_colour,'solid','circle']
                except:
                    appendthis = [row['id'],'data_label',l,0,0,'','']
                limit_data.append(appendthis)
        #lol
    print('parsed limit data >>>>',limit_data) 
    
    ## the datatable needed a unique id
    ## the id of the limit table was renamed to limit_id
    ## a new column was created called id
    
    limit_data_df_out = pd.DataFrame(data=limit_data,columns=['id','data_label','trace_id','raw_x','raw_y','color','line', 'symbol'])
    limit_data_df_out['masses'] = limit_data_df_out['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out['cross_sections'] = limit_data_df_out['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out = limit_data_df_out.rename(columns={"id": "limit_id" })
    limit_data_df_out = limit_data_df_out.reset_index()
    limit_data_df_out['id'] = limit_data_df_out.index
    limit_data_df_out.set_index('id', inplace=True, drop=False)
    
    #columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']

    limit_list_df_out = limit_data_df_out[['limit_id','data_label']].copy()
    limit_list_df_out.drop_duplicates(inplace=True)
    limit_list_df_out = limit_list_df_out.reset_index()
    limit_list_df_out['id'] = limit_list_df_out.index
    limit_list_df_out.set_index('id', inplace=True, drop=False)
    
    trace_list_df_out = limit_data_df_out[['limit_id','data_label','trace_id','color','line','symbol']]
    trace_list_df_out.drop_duplicates(inplace=True)
    trace_list_df_out = trace_list_df_out.reset_index()
    trace_list_df_out['id'] = trace_list_df_out.index
    trace_list_df_out.set_index('id', inplace=True, drop=False)
        
    return limit_list_df_out, trace_list_df_out, limit_data_df_out



def GetLimit(limit_id_in):
    #api_container = "container_fastapi_orm_1:8008"
    fastapi_orm_url = "http://35.214.16.124:8008"
    fastapi_orm_url_api = fastapi_orm_url +"/apiorm"
    url = fastapi_orm_url_api + "/limit/" + str(limit_id_in)
    r = requests.get(url)
    response_data = r.json()
    #print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']

    print('limit_list_df >>', limit_list_df_resp)
    print('trace_list_df >>', trace_list_df_resp)
    print('limit_data_df >>', limit_data_df_resp)

    
    if response_data_frame.empty:
        limit_columns = ['id','limit_id','data_label']
        limit_empty_data = [['id','limit_id','data_label']]
        trace_columns = ['id','limit_id','data_label','trace_id','color','line','symbol']
        trace_empty_data = [['id','limit_id','data_label','trace_id','trace_color']]
        limit_data_columns = ['id','limit_id','data_label','trace_id','raw_x','raw_y','color','line','symbol','masses','cross_sections']
        limit_data_empty_data = [['id','limit_id','data_label','trace_id','raw_x','raw_y','color','line','symbol','masses','cross_sections']]
        #limit_list_df_ret = pd.DataFrame(data=limit_empty_data, columns=limit_columns)
        #trace_list_df_ret = pd.DataFrame(data=trace_empty_data, columns=trace_columns)
        #limit_data_df_ret = pd.DataFrame(data=limit_data_empty_data, columns=limit_data_columns)
        limit_list_df_ret = pd.DataFrame(columns=limit_columns)
        trace_list_df_ret = pd.DataFrame(columns=trace_columns)
        limit_data_df_ret = pd.DataFrame(columns=limit_data_columns)
        
        limit_list_dict_ret = limit_list_df.to_dict('records')
    else:
        limit_list_df_ret = limit_list_df_resp
        trace_list_df_ret = trace_list_df_resp
        limit_data_df_ret = limit_data_df_resp
        limit_list_dict_ret = limit_list_df_ret.to_dict('records')

    return limit_list_df_ret, trace_list_df_ret, limit_data_df_ret, limit_list_dict_ret

def GetLimits():
    #api_container = "container_fastapi_orm_1:8008"
    fastapi_orm_url = "http://35.214.16.124:8008"
    fastapi_orm_url_api = fastapi_orm_url +"/apiorm"
    url = fastapi_orm_url_api + "/limit/"
    r = requests.get(url)
    response_data = r.json()
    #print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']

    print('limit_list_df >>', limit_list_df_resp)
    print('trace_list_df >>', trace_list_df_resp)
    print('limit_data_df >>', limit_data_df_resp)

    
    if response_data_frame.empty:
        limit_columns = ['id','limit_id','data_label']
        limit_empty_data = [['id','limit_id','data_label']]
        trace_columns = ['id','limit_id','data_label','trace_id','color','line','symbol']
        trace_empty_data = [['id','limit_id','data_label','trace_id','color','line','symbol']]
        limit_data_columns = ['id','limit_id','data_label','trace_id','raw_x','raw_y','color','line','symbol','masses','cross_sections']
        limit_data_empty_data = [['id','limit_id','data_label','trace_id','raw_x','raw_y','color','line','symbol','masses','cross_sections']]
        #limit_list_df_ret = pd.DataFrame(data=limit_empty_data, columns=limit_columns)
        #trace_list_df_ret = pd.DataFrame(data=trace_empty_data, columns=trace_columns)
        #limit_data_df_ret = pd.DataFrame(data=limit_data_empty_data, columns=limit_data_columns)
        limit_list_df_ret = pd.DataFrame(columns=limit_columns)
        trace_list_df_ret = pd.DataFrame(columns=trace_columns)
        limit_data_df_ret = pd.DataFrame(columns=limit_data_columns)
        
        limit_list_dict_ret = limit_list_df.to_dict('records')
    else:
        limit_list_df_ret = limit_list_df_resp
        trace_list_df_ret = trace_list_df_resp
        limit_data_df_ret = limit_data_df_resp
        limit_list_dict_ret = limit_list_df_ret.to_dict('records')

    return limit_list_df_ret, trace_list_df_ret, limit_data_df_ret, limit_list_dict_ret


LIMIT_COLUMNS = [
    {"id": "id", "name": "id"},
    {"id": "limit_id", "name": "id"},
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]


def GetLimitDict():
    limit_list_df, trace_list_df, limit_data_df, limit_list_dict = GetLimits()
    return limit_list_dict
