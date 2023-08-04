from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

#from models.models import Song, SongCreate
from models.users import Users, UsersCreate
from models.users import Users_permissions, Users_permissionsCreate
from models.users import User_api_keys, User_api_keysCreate


@router.get("/alembic/users", response_model=list[Users])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(name=song.name, artist=song.artist, year=song.year, id=song.id) for user in users]


@router.post("/alembic/users")
async def add_song(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(name=song.name, artist=song.artist, year=song.year)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/alembic/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.id == user_id)
    results = await session.exec(statement)
    user = results.one()
    await session.delete(user)
    await session.commit()
    return {"deleted": user}
  
