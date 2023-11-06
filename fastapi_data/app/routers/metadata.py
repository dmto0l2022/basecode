from fastapi import Depends, FastAPI
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter
router = APIRouter()

api_base_url = '/dmtool/fastapi_data/'

from typing import List

from db import get_session

from models.metadata import Dropdown_valuepair, Dropdown_valuepairCreate

# Dropdown_valuepairs CRUD

# Fields

#variable
#label
#value
#data_type

@router.get(api_base_url + "dropdown_valuepair", response_model=list[Dropdown_valuepair])
async def get_dropdown_valuepairs(variable_in : str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dropdown_valuepair).where(variable==variable_in))
    dropdown_valuepairs = result.scalars().all()
    return [Dropdown_valuepair(variable=dropdown_valuepair.variable,
                               label=dropdown_valuepair.label,
                               value=dropdown_valuepair.value,
                               data_type=dropdown_valuepair.data_type,
                               id=dropdown_valuepair.id
                              ) for dropdown_valuepair in dropdown_valuepairs]


@router.post(api_base_url + "dropdown_valuepair")
async def add_dropdown_valuepair(dropdown_valuepair: Dropdown_valuepairCreate, session: AsyncSession = Depends(get_session)):
    dropdown_valuepair = Dropdown_valuepair(
                                            variable=dropdown_valuepair.variable,
                                            label=dropdown_valuepair.label,
                                            value=dropdown_valuepair.value,
                                            data_type=dropdown_valuepair.data_type
                                            )
    session.add(dropdown_valuepair)
    await session.commit()
    await session.refresh(dropdown_valuepair)
    return dropdown_valuepair

@router.delete(api_base_url + "dropdown_valuepair/{dropdown_valuepair_id}")
async def delete_dropdown_valuepair(dropdown_valuepair_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Dropdown_valuepair).where(Dropdown_valuepair.id == dropdown_valuepair_id)
    results = await session.exec(statement)
    dropdown_valuepair = results.one()
    await session.delete(dropdown_valuepair)
    await session.commit()
    return {"deleted": dropdown_valuepair}
