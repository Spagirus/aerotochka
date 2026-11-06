"""датакласс дрона"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from scr.domain.enums import DronePurpose, DroneStatus, FlightRank


@dataclass
class Drone:
    sku: str
    name: str
    manufacturer: str
    purpose: DronePurpose
    rank: FlightRank
    weight_g: int
    max_flight_time_min: int
    max_range_m: int
    price: int
    status: DroneStatus = field(default=DroneStatus.in_stock)
    customer_id: uuid.UUID | None = field(default=None)
    has_camera: bool = field(default=False)
    sold_at: datetime | None = field(default=None)
    sold_price: int | None = field(default=None)
    sold_license_id: uuid.UUID | None = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
