"""модуль модельки Покупателя"""

import uuid
from datetime import date, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db import Base
from src.infrastructure.models.utils import get_msk_time


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(12), unique=True)
    email: Mapped[str | None]
    birth_date: Mapped[date] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=get_msk_time, nullable=False)
