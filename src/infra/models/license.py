"""модуль модельки Дрона"""

import uuid
from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import FlightRank, LicenseStatus
from src.infra.db import Base
from src.infra.models.utils import get_key, get_msk_time, get_valid_until


class License(Base):
    __tablename__ = "licenses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(36),unique=True, default=get_key, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customers.id", ondelete="RESTRICT"))
    rank: Mapped[FlightRank] = mapped_column(nullable=False)
    status: Mapped[LicenseStatus] = mapped_column(nullable=False, default=LicenseStatus.ACTIVE)
    issued_at: Mapped[datetime] = mapped_column(nullable=False, default=get_msk_time)
    valid_until: Mapped[date] = mapped_column(nullable=False, default=get_valid_until)
    revoke_reason: Mapped[str | None]
