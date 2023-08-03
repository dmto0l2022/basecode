from sqlmodel import SQLModel, Field
from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String

# Declarative base object
Base = declarative_base()
SQLModel.metadata = Base.metadata

class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass

## Users

class UsersBase(SQLModel):
    authlib_id = fields.CharField(max_length=50, unique=True)
    authlib_provider = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    ceased_at = fields.DatetimeField(auto_now=True)


class Song(UsersBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class UsersCreate(SongBase):
    pass

class Users_authlib(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    test = fields.CharField(max_length=50, unique=False)
    test2 = fields.CharField(max_length=50, unique=False)
    authlib_id = fields.CharField(max_length=50, unique=True)
    authlib_provider = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    ceased_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table="users_authlib"
        ##schema = ""
    
    
User_authlib_Pydantic = pydantic_model_creator(Users_authlib, name="User_authlib")
User_authlibIn_Pydantic = pydantic_model_creator(Users_authlib, name="User_authlibIn", exclude_readonly=True)

class Users_authlib_permissions(models.Model):
    """
    The User permissions model
    """

    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    authorised = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    ceased_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table="users_authlib_permissions"
        ##schema = ""
    
    
User_authlib_permissions_Pydantic = pydantic_model_creator(Users_authlib_permissions, name="User_authlib_permissions")
User_authlib_permissionsIn_Pydantic = pydantic_model_creator(Users_authlib_permissions, name="User_authlib_permissionsIn", exclude_readonly=True)

###

class Users_authlib_count(models.Model):
    count: int

User_authlib_count_Pydantic = pydantic_model_creator(Users_authlib_count, name="User_authlib_count")

##response_model=User_authlib_count_Pydantic


class User_api_keys(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    secret_key = fields.CharField(max_length=255, null=True)
    public_key = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    ceased_at = fields.DatetimeField(auto_now=True)
    user_id = fields.IntField()
    
    class Meta:
        table="user_api_keys"
        ##schema = ""

User_api_key_Pydantic = pydantic_model_creator(User_api_keys, name="User_api_key")
User_api_keyIn_Pydantic = pydantic_model_creator(User_api_keys, name="User_api_keyIn", exclude_readonly=True)


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
