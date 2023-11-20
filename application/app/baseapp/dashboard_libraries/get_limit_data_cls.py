import requests
import json
import pandas as pd
from pandas import json_normalize

import plotly.express as px
from itertools import cycle
palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
palette = cycle(palette_list)


class LimitData:
    def __init__(self, dmtool_userid_in, limit_id_in, list_of_limit_ids_in):
        self.dmtool_userid = dmtool_userid_in
        self.limit_id = limit_id_in
        self.list_of_limit_ids = list_of_limit_ids_in
        self.internal_header = {'dmtool-userid':'999'}
        self.user_header = {'dmtool-userid': str(self.dmtool_userid)}
        self.palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
        self.palette = cycle(palette_list)
        self.fastapi_url_limits = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limits" ## multiple limit operations
        self.fastapi_url_limitstoselect = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limitstoselect" ## multiple limit operations
        self.fastapi_url_limit = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limit/" ## single limit operations
        self.limit_url = self.fastapi_url_limit + str(self.limit_id)
        self.LIMIT_COLUMNS = [{"id": "id", "name": "id"},
                                {"id": "limit_id", "name": "limit_id"},
                                {"id": "data_label", "name": "data_label"},
                                {"id": "data_comment", "name": "data_comment"},
                                {"id": "data_reference", "name": "data_refererence"}]
        '''
        x_units: "string",
        y_units: "string"
        x_rescale: "string"
        y_rescale: "string"

        x_units, y_units, x_rescale, y_rescale
        '''
        
        self.limit_columns = ['id','limit_id','data_label','data_reference','data_comment','x_units', 'y_units', 'x_rescale', 'y_rescale', 'year','experiment','spin_dependency','result_type','official','greatest_hit']
        self.limit_empty_data = [['id','limit_id','data_label','data_reference','data_comment','x_units', 'y_units', 'x_rescale', 'y_rescale','year','experiment','spin_dependency','result_type','official','greatest_hit']]
        self.trace_columns = ['id','limit_id','data_label','trace_id','trace_name',
                             'line_color','symbol_color','fill_color','line','symbol']
        self.trace_empty_data = [['id','limit_id','data_label','trace_id','trace_name','color']]
        self.limit_data_columns = ['id','limit_id','data_label','trace_id','trace_name','x_units', 'y_units', 'x_rescale', 'y_rescale','raw_x','raw_y',
                                  'line_color','symbol_color','fill_color','line','symbol','masses','cross_sections']
        self.limit_data_empty_data = [['id','limit_id','data_label','trace_id','trace_name','x_units', 'y_units', 'x_rescale', 'y_rescale', 'raw_x','raw_y',
                                      'line_color','symbol_color','fill_color','line','symbol','masses','cross_sections']]
        self.limit_list_df = pd.DataFrame(columns=self.limit_columns)
        self.trace_list_df = pd.DataFrame(columns=self.trace_columns)
        self.limit_data_df = pd.DataFrame(columns=self.limit_data_columns)
        self.limit_list_dict = {}
        
        self.limit_data = []
        self.trace_data = []
        self.limits_dataframe = pd.DataFrame()
        #self.ParseLimitData()
        self.GetLimitData()
        self.PopulateLimitList()
        self.PopulateTraceList()
        ##self.PopulateLimitData()

    # Define scale factors
    def get_scale_factor(self, unit_in):
        
        self.BARN_CM2 = 1e-24
        
        if (unit_in == "b"):
            return self.BARN_CM2
        elif (unit_in == "mb"):
            return 1e-3*self.BARN_CM2
        elif (unit_in == "ub"):
            return 1e-6*self.BARN_CM2
        elif (unit_in == "nb"):
            return 1e-9*self.BARN_CM2
        elif (unit_in == "pb"):
            return 1e-12*self.BARN_CM2
        elif (unit_in == "fb"):
            return 1e-15*self.BARN_CM2
        elif (unit_in == "ab"):
            return 1e-18*self.BARN_CM2
        elif (unit_in == "zb"):
            return 1e-21*self.BARN_CM2
        elif (unit_in == "yb"):
            return 1e-24*self.BARN_CM2
        else: 
            return 1
    
    def PopulateLimitData(self):
       
        for index, row in self.limits_dataframe.iterrows():
            #print("Parsing Row")
            #print(row['id'], row['data_values'])
            data_label = row[['data_label']].iloc[0]
            data_reference= row[['data_reference']].iloc[0]
            data_comment = row[['data_comment']].iloc[0]
            x_units = row[['x_units']].iloc[0]
            y_units = row[['y_units']].iloc[0]
            x_rescale = row[['x_rescale']].iloc[0]
            y_rescale = row[['y_rescale']].iloc[0]
            year = row[['year']].iloc[0]
            experiment = row[['experiment']].iloc[0]
            spin_dependency = row[['spin_dependency']].iloc[0]
            result_type = row[['result_type']].iloc[0]
            official = row[['official']].iloc[0]
            greatest_hit = row[['greatest_hit']].iloc[0]
            data_string = row[['data_values']].iloc[0]
            data_string = data_string.replace("{[", "")
            data_string = data_string.replace("]}", "")
            #print(data_string)
            data_series = data_string.split("]")
            #print(len(data_series))
            for l in range(0,len(data_series)):
                next_colour = next(self.palette)
                single_set = data_series[l]
                set_list = single_set.split(";")
                appendthis= []
                for i in set_list:
                    z = i.split(" ");
                    new_x = z[0].replace(",[", "")
                    #limit_id = row['id']
                    try:
                        appendthis = [row['id'],
                                          data_label,
                                          data_reference,
                                          data_comment,
                                          x_units,
                                          y_units,
                                          x_rescale,
                                          y_rescale,
                                          l,
                                          str(l) + '_' + data_label,
                                          year,
                                          experiment,
                                          spin_dependency,
                                          result_type,
                                          official,
                                          greatest_hit,
                                          new_x, ## raw x
                                          z[1], ## raw y
                                          next_colour,
                                          next_colour,
                                          next_colour,
                                          'solid',
                                          'circle']
                    except:
                        appendthis = [row['id'],'data_label','data_reference','data_comment','x_units','y_units','x_rescale','y_rescale',
                                      l,str(l) + '_data_label','year','experiment','spin_dependency','result_type','official','greatest_hit',0,0,'','','','','']
                    
                    self.limit_data.append(appendthis)
            #lol

       
        #print('gld : parsed limit data >>>>',limit_data) 
        
        ## the datatable needed a unique id
        ## the id of the limit table was renamed to limit_id
        ## a new column was created called id

        ## limit data
        
        self.limit_data_df = pd.DataFrame(
            data=self.limit_data,columns=['id','data_label','data_reference', 'data_comment', 'x_units', 'y_units', 'x_rescale', 'y_rescale', 'trace_id','trace_name', 'year','experiment',
                                      'spin_dependency','result_type','official','greatest_hit',
                                      'raw_x','raw_y','line_color','symbol_color',
                                      'fill_color','line', 'symbol'])
        
        x_units = self.limit_data_df.iloc[0]['x_units']
        y_units = self.limit_data_df.iloc[0]['y_units']
        x_scale_factor = self.get_scale_factor(x_units)
        y_scale_factor = self.get_scale_factor(y_units)
        
        self.limit_data_df['masses'] = self.limit_data_df['raw_x'].astype(str).astype(dtype = float, errors = 'ignore') / x_scale_factor
        self.limit_data_df['cross_sections'] = self.limit_data_df['raw_y'].astype(str).astype(dtype = float, errors = 'ignore') / y_scale_factor
        
        self.limit_data_df = self.limit_data_df.rename(columns={"id": "limit_id" })
        #self.limit_data_df = self.limit_data_df.reset_index()
        self.limit_data_df['id'] = self.limit_data_df.index
        #self.limit_data_df.set_index('id', inplace=True, drop=False)
        
        #columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']
        print("self.limit_data_df.head(5) >>>>>>>>>" , self.limit_data_df.head(5))
    
    def PopulateLimitList(self):
        
        self.limit_list_df = self.limits_dataframe[['id','data_label','data_reference', 'data_comment','x_units', 'y_units', 'x_rescale', 'y_rescale',
                                                    'year','experiment','spin_dependency','result_type','official','greatest_hit']].copy()
        self.limit_list_df.drop_duplicates(inplace=True)
        self.limit_list_df = self.limit_list_df.rename(columns={"id": "limit_id" })
        #self.limit_list_df =  self.limit_list_df.reset_index()
        self.limit_list_df['id'] =  self.limit_list_df.index
        #self.limit_list_df.set_index('id', inplace=True, drop=False)

        self.limit_list_dict = self.limit_list_df.to_dict('records')
        
    def PopulateTraceList(self):
        #### trace list
       
        for index, row in self.limits_dataframe.iterrows():
            #print("Parsing Trace Rows")
            #print(row['id'], row['data_values'])
            data_label = row[['data_label']].iloc[0]
            data_string = row[['data_values']].iloc[0]
            data_string = data_string.replace("{[", "")
            data_string = data_string.replace("]}", "")
            #print(data_string)
            data_series = data_string.split("]")
            #print(len(data_series))
            for l in range(0,len(data_series)):
                next_colour = next(self.palette)
                single_set = data_series[l]
                set_list = single_set.split(";")
                try:
                   appendthis = [row['id'],
                                          data_label,
                                          l, ## trace_id
                                          str(l) + '_' + data_label, ## trace_name
                                          next_colour,
                                          next_colour,
                                          next_colour,
                                          'solid',
                                          'circle']
                except:
                        appendthis = [row['id'],'data_label',l,0,0,'','']
                    
                self.trace_data.append(appendthis)
            #lol
        
        self.trace_list_df = pd.DataFrame(data=self.trace_data, columns = ['limit_id','data_label','trace_id','trace_name',
                                               'line_color','symbol_color','fill_color','line','symbol'])
        
        self.trace_list_df.drop_duplicates(inplace=True)
        #self.trace_list_df = self.trace_list_df.reset_index()
        self.trace_list_df['id'] = self.trace_list_df.index
        #self.trace_list_df.set_index('id', inplace=True, drop=False)
        print("trace list data 5 >>>>>> ", self.trace_list_df.head(5))
    
    def GetLimitData(self):
        
        if self.limit_id != 0:

            ## get one limit of data
            
            response_data_frame = pd.DataFrame()
           
            try:
                r = requests.get(self.limit_url,headers=self.user_header)
                response_data = r.json()
                #print("gld : response_data json >>>>" , response_data)
                response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
                self.limits_dataframe = response_data_frame
                #print("gld : library response_data_frame >>>>>" , response_data_frame)
                
                #self.PopulateLimitData()
                #column_names=['id','data_label','data_comment','data_values']
            
                #print('limit_list_df >>', self.limit_list_df.head(1))
                #print('trace_list_df >>', self.trace_list_df.head(1))
                #print('limit_data_df >>', self.limit_data_df.head(1))
            except:
                a = 1
            
            if response_data_frame.empty:
                print("Get One Limit Data Class - No Response Data")
        
    
        elif (self.limit_id == 0 and self.list_of_limit_ids == []):
    
            #def GetAllOwnedLimits(dmtool_userid):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> get all owned limits called <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("limit id >>>>" , self.limit_id, "list_of_limit_ids>>>>>> ", self.list_of_limit_ids)
            #limits_url = fastapi_url_limits
            #request_header = {'dmtool-userid':str(dmtool_userid)}
            #response_data_frame = pd.DataFrame()
            #limit_list_df_resp = pd.DataFrame()
            #trace_list_df_resp = pd.DataFrame()
            #limit_data_df_resp = pd.DataFrame()
                
            try:
                #print("get all owned limits url >>>>>>>>>>>> " ,self.fastapi_url_limits)
                r = requests.get(self.fastapi_url_limits, headers=self.user_header)
                response_data = r.json()
                #print("get all owned limits response data json >>>>>>>>>>>> ", response_data)
            
                #print('response data')
                #print('===================')
                #print(response_data)
                #print('===== response data frame ==============')
                response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
                self.limits_dataframe = response_data_frame
                #print('===== response data frame ==============')
                
                #print("gld : library response_data_frame >>>>>" , response_data_frame)
                
                #limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)           
        
                #print('limit_list_df >>', self.limit_list_df.head(1))
                #print('trace_list_df >>', self.trace_list_df.head(1))
                #print('limit_data_df >>', limit_data_df_resp.head(1))
            except:
                a = 1
            
            if response_data_frame.empty:
                print("GetAllOwnedLimits empty")
    
        elif (self.list_of_limit_ids != []):
            
            ##def GetListOfLimits(dmtool_userid,listoflimits_in):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> get list of limits called <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            fastapi_url_listoflimits = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/listoflimits" ## multiple limit operations
            request_header = {'dmtool-userid':str(self.dmtool_userid)}
            response_data_frame = pd.DataFrame()
                
            #try:
            print("get limits - list of limits ", self.list_of_limit_ids)
            listoflimits_json = {"limit_ids": self.list_of_limit_ids}
            
            r = requests.post(fastapi_url_listoflimits,json=listoflimits_json,  headers=request_header)
            response_data = r.json()
            #print("list of limits request response >>>>>>>>>>>>>>>>>>>>> " ,response_data)
        
            #print('response data')
            #print('===================')
            #print(response_data)
            print('===== response data frame ==============')
            response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
            #print('===== response data frame ==============')
            
            #print("gld : library response_data_frame >>>>>" , response_data_frame)
            
            #limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
            #column_names=['id','data_label','data_comment','data_values']

            self.limits_dataframe = response_data_frame
            #print('===== response data frame ==============')
            
            #print('limit_list_df >>', limit_list_df_resp)
            #print('trace_list_df >>', trace_list_df_resp)
            #print('limit_data_df >>', limit_data_df_resp)
            #except:
            #    a = 1
            
            if response_data_frame.empty:
                print("List of Limits Response empty")
        
