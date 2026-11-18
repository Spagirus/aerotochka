"""ендпоинты дрона"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependens import drone_dep
from src.application.schemas.drone import CreateDrone, PaginationDrone, PurchaseDrone, ReadDrone, UpdateDrone
from src.application.schemas.part import PaginationPart
from src.domain.enums import DronePurpose, DroneStatus, FlightRank

router = APIRouter(
    tags=["Drones"],
    prefix="/api/v1/drones"
)


@router.get("/{drone_id}")
async def get_drone(drone_id: UUID, service: drone_dep) -> ReadDrone:
    return await service.get_drone(drone_id=drone_id)


@router.post("", status_code=201)
async def add_drone(data: CreateDrone, service: drone_dep) -> ReadDrone:
    return await service.add_drone(data)


@router.patch("/{drone_id}")
async def patch_drone(drone_id: UUID, service: drone_dep, data: UpdateDrone) -> ReadDrone:
    return await service.update_drone(drone_id=drone_id, data=data)


@router.post("/{drone_id}/purchase")
async def purchase_drone(drone_id: UUID, service: drone_dep, data: PurchaseDrone) -> ReadDrone:
    return await service.purchase_drone(customer_id=data, drone_id=drone_id)


@router.get("")
async def get_drones(
        service: drone_dep,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        purpose: DronePurpose | None = None,
        rank: FlightRank | None = None,
        max_rank: FlightRank | None = None,
        status: DroneStatus | None = None,
        manufacturer: str | None = None,
        has_camera: bool | None = None,
        min_price: Annotated[int | None, Query(ge=1)] = None,
        max_price: Annotated[int | None, Query(ge=1)] = None,
        customer_id: UUID | None = None,
) -> PaginationDrone:

    return await service.get_drones(
            limit=limit,
            offset=offset,
            purpose=purpose,
            rank=rank,
            max_rank=max_rank,
            status=status,
            manufacturer=manufacturer,
            has_camera=has_camera,
            customer_id=customer_id,
            min_price=min_price,
            max_price=max_price
    )

@router.get("/{drone_id}/parts")
async def get_parts_drone(
        service: drone_dep,
        drone_id: UUID,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        ) -> PaginationPart:
    return await service.get_parts_drone(drone_id=drone_id, limit=limit, offset=offset)
