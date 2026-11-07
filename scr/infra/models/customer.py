"""модуль модельки Покупателя"""

import uuid
from datetime import date, datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from scr.infra.db import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(12))
    email: Mapped[str | None]
    birth_date: Mapped[date] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


