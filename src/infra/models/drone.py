"""модуль модельки Дрона"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.enums import DronePurpose, DroneStatus, FlightRank
from src.infra.db import Base


class Drone(Base):
    __tablename__ = "Drones"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sku: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    purpose: Mapped[DronePurpose] = mapped_column(nullable=False)
    rank: Mapped[FlightRank] = mapped_column(nullable=False)
    weight_g: Mapped[int] = mapped_column(nullable=False)
    max_flight_time_min: Mapped[int] = mapped_column(nullable=False)
    max_range_m: Mapped[int] = mapped_column(nullable=False)
    has_camera: Mapped[bool] = mapped_column(nullable=False, default=False)
    price: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[DroneStatus] = mapped_column(nullable=False, server_default=DroneStatus.IN_STOCK)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("Customers.id"))
    sold_at: Mapped[datetime | None]
    sold_price: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    __table_args__ = (
        CheckConstraint("weight_g > 0", name="weight_g_positive"),
        CheckConstraint("max_flight_time_min > 0", name="flight_time_positive"),
        CheckConstraint("max_range_m > 0", name="max_range_positive"),
        CheckConstraint("price > 0", name="drone_price_positive"),
        CheckConstraint("sold_price > 0", name="sold_price_positive"),
    )
