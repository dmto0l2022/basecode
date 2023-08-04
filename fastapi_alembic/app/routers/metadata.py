from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

from typing import List

from db import get_session

from models.metadata import Dropdown_valuepairs, Dropdown_valuepairsCreate

# Dropdown_valuepairs CRUD

# Fields

#variable
#label
#value
#data_type

@router.get("/alembic/dropdown_valuepairs", response_model=list[Dropdown_valuepairs])
async def get_dropdown_valuepairs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dropdown_valuepairs))
    dropdown_valuepairs = result.scalars().all()
    return [dropdown_valuepair(variable=dropdown_valuepair.variable,
                               label=dropdown_valuepair.label,
                               variable=dropdown_valuepair.variable,
                               value=dropdown_valuepair.value,
                               data_type=dropdown_valuepair.data_type,
                               id=dropdown_valuepair.id
                              ) for dropdown_valuepair in dropdown_valuepairs]


@router.post("/alembic/dropdown_valuepairs")
async def add_dropdown_valuepair(dropdown_valuepair: Dropdown_valuepairsCreate, session: AsyncSession = Depends(get_session)):
    dropdown_valuepair = dropdown_valuepair(
                                            variable=dropdown_valuepair.variable,
                                            label=dropdown_valuepair.label,
                                            variable=dropdown_valuepair.variable,
                                            value=dropdown_valuepair.value,
                                            data_type=dropdown_valuepair.data_type
                                            )
    session.add(dropdown_valuepair)
    await session.commit()
    await session.refresh(dropdown_valuepair)
    return dropdown_valuepair

@router.delete("/alembic/dropdown_valuepairs/{dropdown_valuepair_id}")
async def delete_dropdown_valuepair(dropdown_valuepair_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Dropdown_valuepairs).where(Dropdown_valuepairs.id == dropdown_valuepair_id)
    results = await session.exec(statement)
    dropdown_valuepair = results.one()
    await session.delete(dropdown_valuepair)
    await session.commit()
    return {"deleted": dropdown_valuepair}
