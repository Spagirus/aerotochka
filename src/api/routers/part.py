"""ендпоинты покупателя"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependens import part_dep
from src.application.schemas.part import CreatePart, PaginationPart, ReadPart, UpdatePart
from src.domain.enums import DronePurpose

router = APIRouter(
    tags=["Parts"],
    prefix="/api/v1/parts"
)


@router.get("/{part_id}")
async def get_part(part_id: UUID, service: part_dep) -> ReadPart:
    return await service.get_part(part_id=part_id)


@router.post("", status_code=201)
async def add_part(data: CreatePart, service: part_dep) -> ReadPart:
    return await service.add_part(data)


@router.patch("/{part_id}")
async def patch_part(part_id: UUID, service: part_dep, data: UpdatePart) -> ReadPart:
    return await service.update_part(part_id=part_id, data=data)


@router.get("")
async def get_parts(
        service: part_dep,
        purpose: DronePurpose | None = None,
        attached: bool | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        ) -> PaginationPart:
    return await service.get_parts(purpose=purpose, attached=attached, limit=limit, offset=offset)

@router.delete("/{part_id}", status_code = 204)
async def delete_part(part_id: UUID, service: part_dep) -> None:
    return await service.delete_part(part_id=part_id)
