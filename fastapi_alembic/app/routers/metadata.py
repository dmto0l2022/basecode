from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

from models.models import Song, SongCreate

@router.get("/alembic/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@router.post("/alembic/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song

@router.delete("/alembic/songs/{song_id}")
async def delete_song(song_id: int, session: AsyncSession = Depends(get_session)):
    #song = session.get(Song, song_id) ## works on the primary key of the table
    statement = select(Song).where(Song.id == song_id)
    results = await session.exec(statement)
    song = results.one()
    await session.delete(song)
    await session.commit()
    return {"deleted": song}

