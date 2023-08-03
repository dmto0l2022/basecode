from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

from models.models import Song, SongCreate

@router.get("/alembic/ping")
async def pong():
    return {"ping": "pong!"}

