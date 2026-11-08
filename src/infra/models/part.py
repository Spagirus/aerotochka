"""Модуль модельки Запчасти"""

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.enums import DronePurpose


class Part(Base):
    __tablename__ = "Parts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    purpose: Mapped[DronePurpose] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    drone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("Drones.id"))

    __table_args__ = (
        CheckConstraint("price > 0", name="part_price_positive")
    )
