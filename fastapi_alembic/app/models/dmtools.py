from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Experiments(models.Model):
    """
    The Experiments model
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    
    class Meta:
        table="experiments"
        ##schema = ""

Experiment_Pydantic = pydantic_model_creator(Experiments, name="Experiment")
ExperimentIn_Pydantic = pydantic_model_creator(Experiments, name="ExperimentsIn", exclude_readonly=True)        
        
class Limit_Display(models.Model):
    
    id = fields.IntField(pk=True)
    limit_id = fields.IntField(pk=False)
    plot_id = fields.IntField(pk=False)
    trace_id = fields.IntField(pk=False) ## new field
    symbol = fields.CharField(max_length=255) ## new field
    symbol_color = fields.CharField(max_length=255) ## new field
    line_style = fields.CharField(max_length=255) ## new field
    line_color = fields.CharField(max_length=255) ## new field
    fill_color = fields.CharField(max_length=255) ## new field
    color = fields.CharField(max_length=255) ## legacy field
    style = fields.CharField(max_length=255) ## legacy field
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table="limit_display"
        ##schema = ""

Limit_Display_Pydantic = pydantic_model_creator(Limit_Display, name="Limit_Display")
Limit_DisplayIn_Pydantic = pydantic_model_creator(Limit_Display, name="Limit_DisplayIn", exclude_readonly=True)      
        
class Limit_Ownership(models.Model):    
    
    id = fields.IntField(pk=True)
    user_id = fields.IntField(pk=False)
    limit_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table="limit_ownership"
        ##schema = ""

Limit_Ownership_Pydantic = pydantic_model_creator(Limit_Ownership, name="Limit_Ownership")
Limit_OwnershipIn_Pydantic = pydantic_model_creator(Limit_Ownership, name="Limit_OwnershipIn", exclude_readonly=True)      
         
        
class Limits(models.Model):  
    
    id = fields.IntField(pk=True)
    spin_dependency = fields.CharField(max_length=255)
    result_type = fields.CharField(max_length=255)
    measurement_type = fields.CharField(max_length=60)
    nomhash = fields.CharField(max_length=255)
    x_units = fields.CharField(max_length=255)
    y_units = fields.CharField(max_length=255)
    x_rescale = fields.CharField(max_length=255)
    y_rescale = fields.CharField(max_length=255)
    default_color = fields.CharField(max_length=255)
    default_style = fields.CharField(max_length=255)
    data_values = fields.TextField()
    data_label = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)
    data_comment = fields.CharField(max_length=255)
    data_reference = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    creator_id = fields.IntField(pk=False)
    experiment = fields.CharField(max_length=255)
    rating = fields.IntField(pk=False)
    date_of_announcement = fields.DateField(auto_now_add=False)
    public = fields.BooleanField()
    official = fields.BooleanField()
    date_official = fields.DateField(auto_now_add=False)
    greatest_hit = fields.BooleanField()
    date_of_run_start = fields.DateField(auto_now_add=False)
    date_of_run_end = fields.DateField(auto_now_add=False)
    year = fields.IntField(pk=False)
    
    class Meta:
        table="limits"
        ##schema = ""

Limit_Pydantic = pydantic_model_creator(Limits, name="Limit")
LimitIn_Pydantic = pydantic_model_creator(Limits, name="LimitIn", exclude_readonly=True)      
        
class Plot_Ownership(models.Model):      
    
    id = fields.IntField(pk=True)
    user_id = fields.IntField(pk=False)
    plot_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table="plot_ownership"
        ##schema = ""

Plot_Ownership_Pydantic = pydantic_model_creator(Plot_Ownership, name="Plot_Ownership")
Plot_OwnershipIn_Pydantic = pydantic_model_creator(Plot_Ownership, name="Plot_OwnershipIn", exclude_readonly=True)   

class Plots(models.Model):      
    
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    x_min = fields.CharField(max_length=255)
    x_max = fields.CharField(max_length=255)
    y_min = fields.CharField(max_length=255)
    y_max = fields.CharField(max_length=255)
    x_units = fields.CharField(max_length=255)
    y_units = fields.CharField(max_length=255)
    user_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    plot_png = fields.TextField()
    legend_png = fields.TextField()
    plot_eps = fields.TextField()
    legend_eps = fields.TextField()
    no_id = fields.IntField(pk=False)

    class Meta:
        table="plots"
        ##schema = ""

Plot_Pydantic = pydantic_model_creator(Plots, name="Plot")
PlotIn_Pydantic = pydantic_model_creator(Plots, name="PlotIn", exclude_readonly=True)  
