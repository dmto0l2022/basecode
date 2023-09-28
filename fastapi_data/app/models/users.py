from sqlmodel import SQLModel, Field
from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import String

import uuid

from datetime import datetime

datetime_origin_str = '01/01/1980 00:00:00'

datetime_origin = datetime.strptime(datetime_origin_str, '%m/%d/%Y %H:%M:%S')


# Declarative base object
#Base = declarative_base()
#SQLModel.metadata = Base.metadata

from models.base import Base
SQLModel.metadata = Base.metadata

#name: str = Field(default=None)
#limit_id : int = Field(default=None, nullable=False, primary_key=False)
#symbol : str = Field(default=None)
#created_at : datetime = Field(default=datetime.utcnow(), nullable=False)

## Classes
#User, UserCreate
#User_permission, User_permissionCreate
#User_api_key, User_api_keyCreate

## Users

# Fields
#authlib_id
#authlib_provider
#created_at
#modified_at
#ceased_at

class UserBase(SQLModel):
    authlib_id : str = Field(default=None)
    authlib_provider : str = Field(default=None)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    modified_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime_origin, nullable=False)


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class UserCreate(UserBase):
    pass

## User_permission
# Fields
# user_id
# authorised
# created_at
# modified_at
# ceased_at

class User_permissionBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    authorised : int = Field(default=None, nullable=False, primary_key=False)
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    modified_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime_origin, nullable=False)

class User_permission(User_permissionBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class User_permissionCreate(User_permissionBase):
    pass

## User_api_keys
# Fields
# user_id
# secret_key
# public_key
# created_at
# modified_at
# ceased_at

class User_api_keyBase(SQLModel):
    user_id : int = Field(default=None, nullable=False, primary_key=False)
    api_key : str = Field(default=uuid.uuid1())
    encrypted_api_key : str = Field(default=uuid.uuid1())
    public_key : str = Field(default=uuid.uuid1())
    private_key : str = Field(default=uuid.uuid1())
    created_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    modified_at : datetime = Field(default=datetime.utcnow(), nullable=False)
    ceased_at : datetime = Field(default=datetime_origin, nullable=False)

class User_api_key(User_api_keyBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class User_api_keyCreate(User_api_keyBase):
    user_id : int = Field(default=None, nullable=False, primary_key=False)

class User_api_keyUpdate(SQLModel):
    user_id : Optional[int]= None
    api_key : Optional[int]= None
    encrypted_api_key : Optional[int]= None
    public_key : Optional[str] = None
    private_key : Optional[str] = None
    created_at : Optional[datetime] = None
    modified_at : Optional[datetime] = None
    ceased_at : datetime = Field(default=datetime.utcnow(), nullable=False)

'''
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
'''
