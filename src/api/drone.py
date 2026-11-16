"""ендпоинты дрона"""
from uuid import UUID

from fastapi import APIRouter

from src.api.dependens import drone_dep
from src.application.schemas.drone import CreateDrone, ReadDrone, UpdateDrone, PurchaseDrone

router = APIRouter(
    tags=["Drones"],
    prefix="/api/v1/drones"
)


@router.get("/{id}")
async def get_drone(drone_id: UUID, service: drone_dep) -> ReadDrone:
    return await service.get_drone(drone_id=drone_id)


@router.post("/", status_code=201)
async def add_drone(data: CreateDrone, service: drone_dep) -> ReadDrone:
    return await service.add_drone(data)


@router.patch("/{drone_id}")
async def patch_drone(drone_id: UUID, service: drone_dep, data: UpdateDrone) -> ReadDrone:
    return await service.update_drone(drone_id=drone_id, data=data)


@router.post("/{drone_id}/purchase")
async def purchase_drone(drone_id: UUID, service: drone_dep, data: PurchaseDrone) -> ReadDrone:
    return await service.purchase_drone(customer_id=data, drone_id=drone_id)