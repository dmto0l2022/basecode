from fastapi import APIRouter
router = APIRouter()

from typing import List

from models.users import User_Pydantic, UserIn_Pydantic, Users
from models.users import User_authlib_Pydantic, User_authlibIn_Pydantic, Users_authlib
from models.users import User_authlib_count_Pydantic

from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

class Status(BaseModel):
    message: str




