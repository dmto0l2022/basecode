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


from models.base import Base
SQLModel.metadata = Base.metadata

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

