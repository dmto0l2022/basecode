from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session, init_db
from models.models import Song, SongCreate

app = FastAPI(title="DMTOOL API Server - Alembic",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url="/alembic/openapi.json",
              docs_url="/alembic/docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )



@app.get("/alembic/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/alembic/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/alembic/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
