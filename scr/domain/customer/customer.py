"""датакласс покупателя"""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Customer:
    full_name: str
    phone: str
    email: str | None
    birth_date: date
    created_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)



