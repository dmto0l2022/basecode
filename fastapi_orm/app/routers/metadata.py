from fastapi import APIRouter
router = APIRouter()

from typing import List

from models.metadata import dropdown_valuepair_Pydantic, dropdown_valuepairIn_Pydantic, dropdown_valuepairs

from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

class Status(BaseModel):
    message: str

#### value pairs #####

@router.get("/apiorm/metadata", response_model=List[dropdown_valuepair_Pydantic])
async def get_pairs():
    return await dropdown_valuepair_Pydantic.from_queryset(dropdown_valuepairs.all())


@router.post("/apiorm/metadata", response_model=dropdown_valuepair_Pydantic)
async def create_pair(pair: dropdown_valuepairIn_Pydantic):
    pair_obj = await dropdown_valuepairs.create(**pair.dict(exclude_unset=True))
    return await dropdown_valuepair_Pydantic.from_tortoise_orm(pair_obj)


@router.get(
    "/apiorm/metadata/{id}", response_model=dropdown_valuepair_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_pair(id: int):
    return await dropdown_valuepair_Pydantic.from_queryset_single(dropdown_valuepairs.get(id=id))


@router.put(
    "/apiorm/metadata/{user_id}", response_model=dropdown_valuepair_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_pair(id: int, pair: dropdown_valuepairIn_Pydantic):
    await dropdown_valuepairs.filter(id=id).update(**pair.dict(exclude_unset=True))
    return await dropdown_valuepair_Pydantic.from_queryset_single(dropdown_valuepairs.get(id=id))


@router.delete("/apiorm/metadata/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_pair(id: int):
    deleted_count = await dropdown_valuepairs.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Pair {id} not found")
    return Status(message=f"Deleted pair {id}")

