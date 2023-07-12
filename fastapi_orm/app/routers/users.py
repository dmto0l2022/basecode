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

#### users #####

@router.get("/apiorm/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post("/apiorm/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/apiorm/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.put(
    "/apiorm/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete("/apiorm/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


### authlib users ###

@router.get("/apiorm/authlibusers", response_model=List[User_authlib_Pydantic])
async def get_authlibusers():
    return await User_authlib_Pydantic.from_queryset(Users_authlib.all())


@router.post("/apiorm/authlibusers", response_model=User_authlib_Pydantic)
async def create_authlibuser(userauthlib: User_authlibIn_Pydantic):
    user_authlib_obj = await Users_authlib.create(**userauthlib.dict(exclude_unset=True))
    return await User_authlib_Pydantic.from_tortoise_orm(user_authlib_obj)

#### google users

@router.post("/apiorm/authlibusers/google", response_model=User_authlib_Pydantic)
async def create_authlibuser(userauthlib: User_authlibIn_Pydantic):
    user_authlib_obj = await Users_authlib.create(**userauthlib.dict(exclude_unset=True))
    return await User_authlib_Pydantic.from_tortoise_orm(user_authlib_obj)

@router.get(
    "/apiorm/authlibuser/google/{google_id}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_authlibuser(google_id: str):
    return await User_authlib_Pydantic.from_queryset_single(Users_authlib.get(google_id=google_id))

@router.get(
    "/apiorm/authlibuser/google/exists/{google_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def get_authlibuser_count(google_id: str):
    user_count = await Users_authlib.filter(google_id=google_id).count()
    return Status(message=f"usercount : {user_count}")
    

@router.put(
    "/apiorm/authlibusers/google/{google_id}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_authlibuser(google_id: str, user_authlib: User_authlibIn_Pydantic):
    await Users_authlib.filter(google_id=google_id).update(**user_authlib.dict(exclude_unset=True))
    return await Users_authlib_Pydantic.from_queryset_single(Users_authlib.get(google_id=google_id))


@router.delete("/apiorm/authlibuser/google/{google_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_authlibuser(google_id: str):
    deleted_count = await Users_authlib.filter(google_id=google_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib {google_id} not found")
    return Status(message=f"Deleted authlib user {google_id}")

#### github users

@router.get(
    "/apiorm/authlibuser/github/{github_login}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_authlibuser(github_login: str):
    return await User_authlib_Pydantic.from_queryset_single(Users_authlib.get(github_login=github_login))

@router.get(
    "/apiorm/authlibuser/github/exists/{github_login}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def get_authlibuser_count(github_login: str):
    user_count = await Users_authlib.filter(github_login=github_login).count()
    return Status(message=f"usercount : {user_count}")
    

@router.put(
    "/apiorm/authlibusers/github/{github_login}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_authlibuser(github_login: str, user_authlib: User_authlibIn_Pydantic):
    await Users_authlib.filter(github_login=github_login).update(**user_authlib.dict(exclude_unset=True))
    return await Users_authlib_Pydantic.from_queryset_single(Users_authlib.get(github_login=github_login))


@router.delete("/apiorm/authlibuser/github/{github_login}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_authlibuser(github_login: str):
    deleted_count = await Users_authlib.filter(github_login=github_login).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib {github_login} not found")
    return Status(message=f"Deleted authlib user {github_login}")

