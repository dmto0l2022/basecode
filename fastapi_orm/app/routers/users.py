from fastapi import APIRouter
router = APIRouter()

from typing import List

from models.users import User_Pydantic, UserIn_Pydantic, Users
from models.users import User_authlib_Pydantic, User_authlibIn_Pydantic, Users_authlib
from models.users import User_authlib_permissions_Pydantic, User_authlib_permissionsIn_Pydantic, Users_authlib_permissions
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

@router.post("/apiorm/authlibuser/google", response_model=User_authlib_Pydantic)
async def create_google_authlibuser(userauthlib: User_authlibIn_Pydantic):
    user_authlib_obj = await Users_authlib.create(**userauthlib.dict(exclude_unset=True))
    return await User_authlib_Pydantic.from_tortoise_orm(user_authlib_obj)

@router.get(
    "/apiorm/authlibuser/google/{google_id}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_google_authlibuser(google_id: str):
    return await User_authlib_Pydantic.from_queryset_single(Users_authlib.get(authlib_id=google_id, authlib_provider='google'))

@router.get(
    "/apiorm/authlibuser/google/exists/{google_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def get_google_authlibuser_count(google_id: str):
    user_count = await Users_authlib.filter(authlib_id=google_id).count()
    return Status(message=f"usercount : {user_count}")
    

@router.put(
    "/apiorm/authlibusers/google/{google_id}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_google_authlibuser(google_id: str, user_authlib: User_authlibIn_Pydantic):
    await Users_authlib.filter(authlib_id=google_id, authlib_provider='google').update(**user_authlib.dict(exclude_unset=True))
    return await Users_authlib_Pydantic.from_queryset_single(Users_authlib.get(authlib_id=google_id, authlib_provider='google'))


@router.delete("/apiorm/authlibuser/google/{google_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_google_authlibuser(google_id: str):
    deleted_count = await Users_authlib.filter(authlib_id=google_id, authlib_provider='google').delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib {google_id} not found")
    return Status(message=f"Deleted authlib user {google_id}")

#### github users

@router.post("/apiorm/authlibuser/github", response_model=User_authlib_Pydantic)
async def create_authlibuser(userauthlib: User_authlibIn_Pydantic):
    user_authlib_obj = await Users_authlib.create(**userauthlib.dict(exclude_unset=True))
    return await User_authlib_Pydantic.from_tortoise_orm(user_authlib_obj)

@router.get(
    "/apiorm/authlibuser/github/{github_login}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_github_authlibuser(github_login: str):
    return await User_authlib_Pydantic.from_queryset_single(Users_authlib.get(authlib_id=github_login, authlib_provider='github'))

@router.get(
    "/apiorm/authlibuser/github/exists/{github_login}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def get_github_authlibuser_count(github_login: str):
    user_count = await Users_authlib.filter(authlib_id=github_login, authlib_provider='github').count()
    return Status(message=f"usercount : {user_count}")
    

@router.put(
    "/apiorm/authlibusers/github/{github_login}", response_model=User_authlib_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_github_authlibuser(github_login: str, user_authlib: User_authlibIn_Pydantic):
    await Users_authlib.filter(authlib_id=github_login, authlib_provider='github').update(**user_authlib.dict(exclude_unset=True))
    return await Users_authlib_Pydantic.from_queryset_single(Users_authlib.get(authlib_id=github_login, authlib_provider='github'))


@router.delete("/apiorm/authlibuser/github/{github_login}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_github_authlibuser(github_login: str):
    deleted_count = await Users_authlib.filter(authlib_id=github_login, authlib_provider='github').delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib {github_login} not found")
    return Status(message=f"Deleted authlib user {github_login}")

#### users permissions

@router.post("/apiorm/authlibuser/permissions", response_model=User_authlib_permissions_Pydantic)
async def create_authlibuser_permissions(userauthlibpermissions: User_authlib_permissionsIn_Pydantic):
    user_authlib_permissions_obj = await Users_authlib_permissions.create(**userauthlibpermissions.dict(exclude_unset=True))
    return await User_authlib_permissions_Pydantic.from_tortoise_orm(user_authlib_permissions_obj)

@router.get(
    "/apiorm/authlibuser/permissions/{user_id}", response_model=User_authlib_permissions_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_authlibuser_permissions(user_id: str):
    return await User_authlib_permissions_Pydantic.from_queryset_single(Users_authlib_permissions.get(user_id=user_id))

@router.put(
    "/apiorm/authlibusers/permissions/{user_id}", response_model=User_authlib_permissions_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_authlibuser_permissions(user_id: str, user_authlib_permissions: User_authlib_permissionsIn_Pydantic):
    await Users_authlib_permissions.filter(user_id=user_id).update(**user_authlib_permissions.dict(exclude_unset=True))
    return await Users_authlib_permissions_Pydantic.from_queryset_single(Users_authlib_permissions.get(user_id=user_id))


@router.delete("/apiorm/authlibuser/permissions/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_authlibuser_permissions(user_id: str):
    deleted_count = await Users_authlib_permissions.filter(user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib_permissions {user_id} not found")
    return Status(message=f"Deleted authlib permissions for user {user_id}")

############ api keys ###################

#User_api_key_Pydantic = pydantic_model_creator(User_api_keys, name="User_api_key")
#User_api_keyIn_Pydantic = pydantic_model_creator(User_api_keys, name="User_api_keyIn", exclude_readonly=True)

@router.post("/apiorm/apikey", response_model=User_api_key_Pydantic)
async def create_userapikey(userapikeys: User_api_keyIn_Pydantic):
    user_apikey_obj = await User_api_keys.create(**userapikeys.dict(exclude_unset=True))
    return await User_api_key_Pydantic.from_tortoise_orm(user_apikey_obj)

@router.get(
    "/apiorm/apikey/{user_id}", response_model=User_api_key_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_userapikey(user_id: str):
    return await User_api_key_Pydantic.from_queryset_single(User_api_keys.get(user_id=user_id))

@router.put(
    "/apiorm/apikey/{user_id}", response_model=User_api_key_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_userapikey(user_id: str, user_authlib_permissions: User_authlib_permissionsIn_Pydantic):
    await Users_authlib_permissions.filter(user_id=user_id).update(**user_authlib_permissions.dict(exclude_unset=True))
    return await Users_authlib_permissions_Pydantic.from_queryset_single(Users_authlib_permissions.get(user_id=user_id))


@router.delete("/apiorm/apikey/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_authlibuser_permissions(user_id: str):
    deleted_count = await Users_authlib_permissions.filter(user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Users_authlib_permissions {user_id} not found")
    return Status(message=f"Deleted authlib permissions for user {user_id}")
