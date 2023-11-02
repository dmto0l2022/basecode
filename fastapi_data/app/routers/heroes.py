from typing import List, Optional

from fastapi import FastAPI, Depends
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


@app.get("/examples/test/teams/", response_model=List[TeamReadWithHeroes])
def get_teams(*, session: Session = Depends(get_session)) -> List[Team]:
    return session.exec(select(Team)).all()
