"""модуль датакласса лицензии"""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime

from utils import get_key, get_valid_until

from scr.domain.enums import FlightRank, LicenseStatus


@dataclass
class License:
    customer_id: uuid.UUID
    rank: FlightRank
    status: LicenseStatus
    valid_until: date = field(default_factory=get_valid_until)
    revoke_reason: str | None = field(default=None)
    issued_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    key: str = field(default_factory=get_key)
