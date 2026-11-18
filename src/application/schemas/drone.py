"""схемы pydantic для дрона"""
from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.domain.enums import DronePurpose, DroneStatus, FlightRank

from .base_schemas import BaseInput, BaseOutput


class CreateDrone(BaseInput):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=200)
    manufacturer: str = Field(min_length=1, max_length=100)
    purpose: DronePurpose
    rank: FlightRank
    weight_g: int = Field(gt=0)
    max_flight_time_min: int = Field(gt=0)
    max_range_m: int = Field(gt=0)
    has_camera: bool = Field(default=False)
    price: int = Field(gt=0)


class ReadDrone(BaseOutput):
    id: UUID
    sku: str
    name: str
    manufacturer: str
    purpose: DronePurpose
    rank: FlightRank
    weight_g: int
    max_flight_time_min: int
    max_range_m: int
    has_camera: bool
    price: int
    status: DroneStatus
    customer_id: UUID | None
    sold_at: datetime | None
    sold_price: int | None
    sold_license_id: UUID | None
    created_at: datetime
    updated_at: datetime


class UpdateDrone(BaseInput):
    sku: str | None = Field(min_length=1, default=None)
    name: str | None = Field(min_length=1, max_length=200, default=None)
    manufacturer: str | None = Field(min_length=1, max_length=100, default=None)
    purpose: DronePurpose | None = None
    rank: FlightRank | None = None
    weight_g: int | None = Field(default=None, gt=0)
    max_flight_time_min: int | None = Field(default=None, gt=0)
    max_range_m: int | None = Field(default=None, gt=0)
    has_camera: bool | None = Field(default=None)
    price: int | None = Field(gt=0, default=None)
    status: DroneStatus | None = None


class PurchaseDrone(BaseInput):
    customer_id: UUID


class PaginationDrone(BaseInput):
    items: list[ReadDrone]
    total: int
    limit: int
    offset: int
