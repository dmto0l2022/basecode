from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Users_authlib(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=20, unique=True)
    email_verified = fields.BooleanField()
    name = fields.CharField(max_length=50, null=True)
    given_name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table="users_authlib"
        ##schema = ""
    
    
User_authlib_Pydantic = pydantic_model_creator(Users_authlib, name="User_authlib")
User_authlibIn_Pydantic = pydantic_model_creator(Users_authlib, name="User_authlibIn", exclude_readonly=True)

###

class Users_authlib_count(models.Model):
    count: int

User_authlib_count_Pydantic = pydantic_model_creator(Users_authlib_count, name="User_authlib_count")

##response_model=User_authlib_count_Pydantic

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
