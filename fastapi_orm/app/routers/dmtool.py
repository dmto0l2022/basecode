from fastapi import APIRouter
router = APIRouter()

from typing import List

from models import Experiment_Pydantic, ExperimentIn_Pydantic, Experiments
from models import Limit_Display_Pydantic, Limit_DisplayIn_Pydantic, Limit_Display
from models import Limit_Ownership_Pydantic, Limit_OwnershipIn_Pydantic, Limit_Ownership   
from models import Limit_Pydantic, LimitIn_Pydantic, Limits
from models import Plot_Ownership_Pydantic, Plot_OwnershipIn_Pydantic, Plot_Ownership
from models import Plot_Pydantic, PlotIn_Pydantic, Plots

from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

#### plot #####

@router.get("/apiorm/plots", response_model=List[Plot_Pydantic])
async def get_plots():
    return await Plot_Pydantic.from_queryset(Plots.all())

@router.post("/apiorm/plot", response_model=Plot_Pydantic)
async def create_plot(plot: PlotIn_Pydantic):
    plot_obj = await Plots.create(**plot.dict(exclude_unset=True))
    return await Plot_Pydantic.from_tortoise_orm(plot_obj)

@router.get(
    "/apiorm/plot/{plot_id}", response_model=Plot_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_plot(plot_id: int):
    return await Plot_Pydantic.from_queryset_single(Plots.get(id=plot_id))

@router.put(
    "/apiorm/plot/{plot_id}", response_model=Plot_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_plot(plot_id: int, plot: PlotIn_Pydantic):
    await Plots.filter(id=plot_id).update(**plot.dict(exclude_unset=True))
    return await Plot_Pydantic.from_queryset_single(Plots.get(id=plot_id))

@router.delete("/apiorm/plot/{plot_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_plot(plot_id: int):
    deleted_count = await Plots.filter(id=plot_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Plot {plot_id} not found")
    return Status(message=f"Deleted Plot {plot_id}")                   
        
        
#### plot ownership #####

@router.get("/apiorm/plot_ownerships", response_model=List[Plot_Ownership_Pydantic])
async def get_plot_ownerships():
    return await Plot_Ownership_Pydantic.from_queryset(Limit.all())

@router.post("/apiorm/plot_ownership", response_model=Plot_Ownership_Pydantic)
async def create_plot_ownership(plot_ownership: Plot_OwnershipIn_Pydantic):
    plot_ownership_obj = await Plot_Ownership.create(**plot_ownership.dict(exclude_unset=True))
    return await Plot_Ownership_Pydantic.from_tortoise_orm(plot_ownership_obj)

@router.get(
    "/apiorm/plot_ownership/{plot_ownership_id}", response_model=Plot_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_plot_ownership(plot_ownership_id: int):
    return await Plot_Ownership_Pydantic.from_queryset_single(Plot_Ownership.get(id=plot_ownership_id))

@router.put(
    "/apiorm/plot_ownership/{plot_ownership_id}", response_model=Plot_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_plot_ownership(plot_ownership_id: int, plot_ownership: Plot_OwnershipIn_Pydantic):
    await Plot_Ownership.filter(id=plot_ownership_id).update(**plot_ownership.dict(exclude_unset=True))
    return await Plot_Ownership_Pydantic.from_queryset_single(Plot_Ownership.get(id=plot_ownership_id))


@router.delete("/apiorm/plot_ownership/{plot_ownership_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit(plot_ownership_id: int):
    deleted_count = await Plot_Ownership.filter(id=plot_ownership_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Plot Ownership {plot_ownership_id} not found")
    return Status(message=f"Deleted Plot Ownership {plot_ownership_id}")        
        
            
        
#### limit #####

@router.get("/apiorm/limit", response_model=List[Limit_Pydantic])
async def get_limits():
    return await Limit_Pydantic.from_queryset(Limits.all())

@router.post("/apiorm/limit", response_model=Limit_Pydantic)
async def create_limit(limit: LimitIn_Pydantic):
    limit_obj = await Limits.create(**limit.dict(exclude_unset=True))
    return await Limit_Pydantic.from_tortoise_orm(limit_obj)

@router.get(
    "/apiorm/limit/{limit_id}", response_model=Limit_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit(limit_id: int):
    return await Limit_Pydantic.from_queryset_single(Limits.get(id=limit_id))

@router.put(
    "/apiorm/limit/{limit_id}", response_model=Limit_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit(limit_id: int, limit: LimitIn_Pydantic):
    await Limits.filter(id=limit_id).update(**limit.dict(exclude_unset=True))
    return await Limit_Pydantic.from_queryset_single(Limits.get(id=limit_id))


@router.delete("/apiorm/limit/{limit_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit(limit_id: int):
    deleted_count = await Limits.filter(id=limit_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit {limit_id} not found")
    return Status(message=f"Deleted Limit {limit_id}")        
        
   
        
#### limit ownership #####

@router.get("/apiorm/limit_ownership", response_model=List[Limit_Ownership_Pydantic])
async def get_limit_ownerships():
    return await Limit_Ownership_Pydantic.from_queryset(Limit_Ownership.all())

@router.post("/apiorm/limit_ownership", response_model=Limit_Ownership_Pydantic)
async def create_limit_ownership(limit_ownership: Limit_OwnershipIn_Pydantic):
    limit_ownership_obj = await Limit_Ownership.create(**limit_ownership.dict(exclude_unset=True))
    return await Limit_Ownership_Pydantic.from_tortoise_orm(limit_ownership_obj)

@router.get(
    "/apiorm/limit_ownership/{limit_ownership_id}", response_model=Limit_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit_ownership(limit_ownership_id: int):
    return await Limit_Ownership_Pydantic.from_queryset_single(Limit_Ownership.get(id=limit_ownership_id))

@router.put(
    "/apiorm/limit_ownership/{limit_ownership_id}", response_model=Limit_Ownership_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit_ownership(limit_ownership_id: int, limit_ownership: Limit_OwnershipIn_Pydantic):
    await Limit_Ownership.filter(id=limit_ownership_id).update(**limit_ownership.dict(exclude_unset=True))
    return await Limit_Ownership_Pydantic.from_queryset_single(Limit_Ownership.get(id=limit_ownership_id))


@router.delete("/apiorm/limit_ownership/{limit_ownership_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit_ownership(limit_ownership_id: int):
    deleted_count = await Limit_Ownership.filter(id=limit_ownership_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit Ownership {limit_ownership_id} not found")
    return Status(message=f"Deleted Limit Ownership {limit_ownership_id}")        
        
#### limit display #####

@router.get("/apiorm/limit_display", response_model=List[Limit_Display_Pydantic])
async def get_limit_displays():
    return await Limit_Display_Pydantic.from_queryset(Limit_Display.all())

@router.post("/apiorm/limit_display", response_model=Limit_Display_Pydantic)
async def create_limit_display(limit_display: Limit_DisplayIn_Pydantic):
    limit_display_obj = await Limit_Display.create(**limit_display.dict(exclude_unset=True))
    return await Limit_Display_Pydantic.from_tortoise_orm(limit_display_obj)

@router.get(
    "/apiorm/limit_display/{limit_display_id}", response_model=Limit_Display_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_limit_display(limit_display_id: int):
    return await Limit_Display_Pydantic.from_queryset_single(Limit_Display.get(id=limit_display_id))

@router.put(
    "/apiorm/limit_display/{limit_display_id}", response_model=Limit_Display_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_limit_display(limit_display_id: int, limit_display: Limit_DisplayIn_Pydantic):
    await Limit_Display.filter(id=limit_display_id).update(**limit_display.dict(exclude_unset=True))
    return await Limit_Display_Pydantic.from_queryset_single(Limit_Display.get(id=limit_display_id))


@router.delete("/apiorm/limit_display/{limit_display_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_limit_display(limit_display_id: int):
    deleted_count = await Limit_Display.filter(id=limit_display_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Limit Display {limit_display_id} not found")
    return Status(message=f"Deleted Limit Display {limit_display_id}")        
        
#### experiments #####

@router.get("/apiorm/experiments", response_model=List[Experiment_Pydantic])
async def get_experiments():
    return await Experiment_Pydantic.from_queryset(Experiments.all())

@router.post("/apiorm/experiments", response_model=Experiment_Pydantic)
async def create_experiment(experiment: ExperimentIn_Pydantic):
    experiment_obj = await Experiments.create(**experiment.dict(exclude_unset=True))
    return await Experiment_Pydantic.from_tortoise_orm(experiment_obj)

@router.get(
    "/apiorm/experiment/{experiment_id}", response_model=Experiment_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_experiment(experiment_id: int):
    return await Experiment_Pydantic.from_queryset_single(Experiments.get(id=experiment_id))

@router.put(
    "/apiorm/experiment/{experiment_id}", response_model=Experiment_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_experiment(experiment_id: int, experiment: ExperimentIn_Pydantic):
    await Experiments.filter(id=experiment_id).update(**experiment.dict(exclude_unset=True))
    return await Experiment_Pydantic.from_queryset_single(Experiments.get(id=experiment_id))


@router.delete("/apiorm/experiment/{experiment_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_experiment(experiment_id: int):
    deleted_count = await Experiments.filter(id=experiment_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Experiment {experiment_id} not found")
    return Status(message=f"Deleted experiment {experiment_id}")
