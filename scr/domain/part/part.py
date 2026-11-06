"""датакласс запчисти"""

import uuid
from dataclasses import dataclass, field

from scr.domain.enums import DronePurpose


@dataclass
class Part:
    name: str
    purpose: DronePurpose
    price: int
    drone_id: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)

