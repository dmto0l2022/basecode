from io import StringIO
import pandas as pd

class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'


class DMTool():
    def __init__(self):
        self.mstring = StringIO("""x,y
          70,50
          90,100
          90,0
          70,0
          70,50
          60,25
          50,0
          30,50
          30,0
          10,0
          10,100
          30,100
          60,25
        """)
        
        self.mdf = pd.read_csv(self.mstring, sep=",")
        
        self.ostring = StringIO("""x,y
          50,0
          65,5
          80,15
          87,30
          90,50
          87,70
          80,90
          65,97
          50,100
          60,85
          65,70
          67,65
          70,50
          67,35
          65,25
          60,12
          50,0
          """)
       
        self.ReadLetterO()
    
        self.tstring = StringIO("""x,y
          10,80
          10,100
          90,100
          90,80
          60,80
          60,0
          40,0
          40,80
          10,80
          """)
    
        self.tdf = pd.read_csv(self.tstring, sep=",")
    
        self.lstring = StringIO("""x,y
          10,0
          100,0
          100,20
          30,20
          30,100
          10,100
          10,0
          """)
    
        self.ldf = pd.read_csv(self.lstring, sep=",")
    
        self.dstring = StringIO("""x,y
          30,0
          65,5
          90,25
          100,50
          90,75
          65,95
          30,100
          60,85
          75,75
          80,50
          75,35
          60,15
          30,0
          10,0
          10,100
          30,100
          30,0
          """)
    
        self.ddf = pd.read_csv(self.dstring, sep=",")
    
        #self.MakeDMTool()
    
    #################################
    def ReadLetterO(self):
        
        odf_stage = pd.read_csv(self.ostring, sep=",")
        
        odf_out = odf_stage.copy()
        
        def reflectx(x_in):
            return 50 - (x_in-50)

        odf_out['x'] = odf_out['x'].apply(reflectx)
        
        #odf_out['x'] = 50 - (odf_out['x']-50)
        
        #odf_out = odf_out.assign(x=50)
        
        odf_out = pd.concat([odf_out, odf_stage],ignore_index=True)
        self.odf = odf_out
   
    def MakeDMTool(self,limit_id_in,trace_id_in):
        
        def add100(x_in):
            return (x_in + 100)
        
        dmtool_out = self.ddf.copy()
        
        dmtool_out['limit_id'] = limit_id_in
        dmtool_out['trace_id'] = trace_id_in
        dmtool_out['trace_name'] = 'd'
        
        #"M"
        df_working = self.mdf.copy()
        df_working['limit_id'] = limit_id_in
        df_working['trace_id'] = trace_id_in + 1
        df_working['trace_name'] = 'm'
        
      

        df_working['x'] = df_working['x'].apply(add100)
        
        dmtool_out = pd.concat([dmtool_out, df_working], ignore_index=True)
        
        #"T"
        
        df_working = self.tdf.copy()
        df_working['limit_id'] = limit_id_in
        df_working['trace_id'] = trace_id_in + 2
        df_working['trace_name'] = 't'

        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        
        dmtool_out = pd.concat([dmtool_out, df_working], ignore_index=True)
        
        #"O1 & O2"
        
        df_working = self.odf.copy()
        df_working['limit_id'] = limit_id_in
        df_working['trace_id'] = trace_id_in + 3
        df_working['trace_name'] = 'o1'

        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        
        dmtool_out = pd.concat([dmtool_out, df_working], ignore_index=True)
        
        df_working['limit_id'] = limit_id_in
        df_working['trace_id'] = trace_id_in + 4
        df_working['trace_name'] = 'o2'
        df_working['x'] = df_working['x'].apply(add100)
        
        dmtool_out = pd.concat([dmtool_out, df_working], ignore_index=True)
        
        #"L"
        
        df_working = self.ldf.copy()
        df_working['limit_id'] = limit_id_in
        df_working['trace_id'] = trace_id_in + 5
        df_working['trace_name'] = 'l'

        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        df_working['x'] = df_working['x'].apply(add100)
        
        dmtool_out = pd.concat([dmtool_out, df_working], ignore_index=True)
        
        ## out
        
        self.dmtdf = dmtool_out
        
