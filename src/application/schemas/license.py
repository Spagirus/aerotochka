from .base_schemas import BaseInput, BaseOutput
from uuid import UUID
from src.domain.enums import FlightRank, LicenseStatus
from datetime import datetime, date

class CreateLicense(BaseInput):
    customer_id: UUID
    rank: FlightRank

class ReadLicense(BaseOutput):
    id: UUID
    key: str
    customer_id: UUID
    rank: FlightRank
    status: LicenseStatus
    issued_at: datetime
    valid_until: date
    revoke_reason: str | None