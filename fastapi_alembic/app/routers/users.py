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

# Users

## Fields
#authlib_id
#authlib_provider
#created_at
#modified_at
#ceased_at


@router.get("/alembic/user", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(id=user.id,
                authlib_id=user.authlib_id,
                authlib_provider=user.authlib_provider,
                created_at=user.created_at,
                modified_at=user.rmodified_at,
                ceased_at=user.ceased_at) for user in users]


@router.post("/alembic/user")
async def add_song(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(authlib_id=user.authlib_id,
                authlib_provider=user.authlib_provider,
                created_at=user.created_at,
                modified_at=user.rmodified_at,
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
  
