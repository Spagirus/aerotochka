"""схемы лицензии"""

from datetime import date, datetime
from uuid import UUID

from src.domain.enums import FlightRank, LicenseStatus


from .base_schemas import BaseInput, BaseOutput


class CreateLicense(BaseInput):
    """схема создания лицензии"""
    customer_id: UUID
    rank: FlightRank


class ReadLicense(BaseOutput):
    """схема ответа лицензии"""
    id: UUID
    key: str
    customer_id: UUID
    rank: FlightRank
    status: LicenseStatus
    issued_at: datetime
    valid_until: date
    revoke_reason: str | None


class RevokeBody(BaseInput):
    """схема тела причины отзыва лицензии"""
    reason: str


class PaginationLicense(BaseInput):
    items: list[ReadLicense]
    total: int
    limit: int
    offset: int
