from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=30, default="misc")
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table="users_tortoise"
        ##schema = ""
    
    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.username

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]
    
User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

class Experiments(models.Model):
    """
    The Experiments model
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

class Limit_Display(models.Model):
    
    id = fields.IntField(pk=True)
    limit_id = fields.IntField(pk=False)
    plot_id = fields.IntField(pk=False)
    color = fields.CharField(max_length=255, unique=True)
    style = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

class Limit_Ownership(models.Model):    
    
    id = fields.IntField(pk=True)
    user_id = fields.IntField(pk=False)
    limit_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

class Limits(models.Model):  
    
    id = fields.IntField(pk=True)
    spin_dependency = fields.CharField(max_length=255, unique=True)
    result_type = fields.CharField(max_length=255, unique=True)
    measurement_type = fields.CharField(max_length=60, unique=True)
    nomhash = fields.CharField(max_length=255, unique=True)
    x_units = fields.CharField(max_length=255, unique=True)
    y_units = fields.CharField(max_length=255, unique=True)
    x_rescale = fields.CharField(max_length=255, unique=True)
    y_rescale = fields.CharField(max_length=255, unique=True)
    default_color = fields.CharField(max_length=255, unique=True)
    default_style = fields.CharField(max_length=255, unique=True)
    data_values = fields.TextField()
    data_label = fields.CharField(max_length=255, unique=True)
    file_name = fields.CharField(max_length=255, unique=True)
    data_comment = fields.CharField(max_length=255, unique=True)
    data_reference = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    creator_id = fields.IntField(pk=False)
    experiment = fields.CharField(max_length=255, unique=True)
    rating = fields.IntField(pk=False)
    date_of_announcement = fields.DateField(auto_now_add=True)
    public = fields.IntField(pk=False)
    official = fields.IntField(pk=False)
    date_official = fields.DateField(auto_now_add=True)
    greatest_hit = fields.IntField(pk=False)
    date_of_run_start = fields.DateField(auto_now_add=True)
    date_of_run_end = fields.DateField(auto_now_add=True)
    year = fields.IntField(pk=False)

class Plot_Ownership(models.Model):      
    
    id = fields.IntField(pk=True)
    user_id = fields.IntField(pk=False)
    plot_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)


class Plots(models.Model):      
    
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    x_min = fields.CharField(max_length=255, unique=True)
    x_max = fields.CharField(max_length=255, unique=True)
    y_min = fields.CharField(max_length=255, unique=True)
    y_max = fields.CharField(max_length=255, unique=True)
    x_units = fields.CharField(max_length=255, unique=True)
    y_units = fields.CharField(max_length=255, unique=True)
    user_id = fields.IntField(pk=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    plot_png = fields.TextField()
    legend_png = fields.TextField()
    plot_eps = fields.TextField()
    legend_eps = fields.TextField()
    no_id = fields.IntField(pk=False)

