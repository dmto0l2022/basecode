from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

#from models.models import Song, SongCreate
from models.users import User, UserCreate
from models.users import User_permission, User_permissionCreate
from models.users import User_api_key, User_api_keyCreate

from datetime import datetime

# Users

## Fields
#authlib_id
#authlib_provider
#created_at
#modified_at
#ceased_at

# User CRUD

@router.get("/alembic/user", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(id=user.id,
                authlib_id=user.authlib_id,
                authlib_provider=user.authlib_provider,
                created_at=user.created_at,
                modified_at=user.modified_at,
                ceased_at=user.ceased_at) for user in users]


@router.post("/alembic/user")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(authlib_id=user.authlib_id,
                authlib_provider=user.authlib_provider,
                created_at=user.created_at,
                modified_at=user.modified_at,
                ceased_at=user.ceased_at)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/alembic/user/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.id == user_id)
    results = await session.exec(statement)
    user = results.one()
    await session.delete(user)
    await session.commit()
    return {"deleted": user}

# User_permission CRUD
## User_permission, User_permissionCreate

# Fields
# id
# user_id
# authorised
# created_at
# modified_at
# ceased_at

@router.get("/alembic/user_permission", response_model=list[User])
async def get_user_permission(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User_permission))
    user_permissions = result.scalars().all()
    return [User_permission(
        id = user_permission.id,
        user_id = user_permission.user_id,
        authorised = user_permission.authorised,
        created_at = user_permission.created_at,
        modified_at = user_permission.modified_at,
        ceased_at = user_permission.ceased_at
    ) for user_permission in user_permissions]


@router.post("/alembic/user_permission")
async def add_user_permission(user_permission: User_permissionCreate, session: AsyncSession = Depends(get_session)):
    user_permission = User_permission(user_id = user_permission.user_id,
        authorised = user_permission.authorised,
        created_at = user_permission.created_at,
        modified_at = user_permission.modified_at,
        ceased_at = user_permission.ceased_at)
    session.add(user_permission)
    await session.commit()
    await session.refresh(user_permission)
    return user_permission

@router.delete("/alembic/user_permission/{user_permission_id}")
async def delete_user_permission(user_permission_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User_permission).where(User_permission.id == user_permission_id)
    results = await session.exec(statement)
    user_permission = results.one()
    await session.delete(user_permission)
    await session.commit()
    return {"deleted": user_permission}


# User_api_key
## User_api_key, User_api_keyCreate
# Fields
# id
# user_id
# secret_key
# public_key
# created_at
# modified_at
# ceased_at

@router.get("/alembic/user_api_keys", response_model=list[User_api_key])
async def get_user_api_keys(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User_api_key))
    user_api_keys = result.scalars().all()
    return [User_api_key(id = user_api_key.id,
                        user_id = user_api_key.user_id,
                        secret_key = user_api_key.secret_key,
                        public_key = user_api_key.public_key,
                        created_at = user_api_key.created_at,
                        modified_at = user_api_key.modified_at,
                        ceased_at = user_api_key.ceased_at
                        ) for user_api_key in user_api_keys]

## get one api key for user

@router.get("/alembic/user_api_key/{user_id}", response_model=User_api_key)
async def get_user_api_key(session: AsyncSession = Depends(get_session)):
    statement = select(User_api_key).where(User_api_key.user_id == user_id)
    user_api_keys = await session.exec(statement)
    user_api_key = user_api_key.one()
    return user_api_key

## add one api key for user

@router.post("/alembic/user_api_key")
async def add_user_api_key(user_api_key: User_api_keyCreate, session: AsyncSession = Depends(get_session)):
    user_api_key = User_api_key(user_id = user_api_key.user_id,
                        secret_key = user_api_key.secret_key,
                        public_key = user_api_key.public_key,
                        created_at = user_api_key.created_at,
                        modified_at = user_api_key.modified_at,
                        ceased_at = user_api_key.ceased_at)
    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)
    return user_api_key

## delete one api key

@router.delete("/alembic/user_api_key/{user_api_key_id}")
async def delete_user_api_key(user_api_key_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id)
    results = await session.exec(statement)
    user_api_key = results.one()
    await session.delete(user_api_key)
    await session.commit()
    return {"deleted": user_api_key}

## cease record

@router.put("/alembic/user_api_key/{user_api_key_id}", response_model=User_api_key)
async def update_user_api_key(user_api_key_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id)
    results = await session.exec(statement)
    user_api_key = results.one()
    await session.delete(user_api_key)
    await session.commit()
    user_api_key = User_api_key(user_id = user_api_key.user_id,
                        secret_key = user_api_key.secret_key,
                        public_key = user_api_key.public_key,
                        created_at = user_api_key.created_at,
                        modified_at = user_api_key.modified_at,
                        ceased_at = datetime.utcnow())
    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)
    return user_api_key
    

@router.patch("/alembic/user_api_key/{user_api_key_id}", response_model=User_api_key)
async def cease_api_key(user_api_key_id: int, user_api_key_in: User_api_keyUpdate, session: AsyncSession = Depends(get_session))):
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id)
    results = await session.exec(statement)
    user_api_key_result = results.one()
    if not user_api_key_result:
        raise HTTPException(status_code=404, detail="Key not found")
    user_api_key_data = user_api_key_in.dict(exclude_unset=True)
    for key, value in user_api_key_data.items():
        setattr(user_api_key_result, key, value)
    session.add(user_api_key_result)
    session.commit()
    session.refresh(user_api_key_result)

