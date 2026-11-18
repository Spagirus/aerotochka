"""схемы для покупателя"""

from uuid import UUID

from pydantic import ConfigDict, Field, field_validator

from src.application.schemas.base_schemas import BaseInput, BaseOutput
from src.domain.enums import DronePurpose


class CreatePart(BaseInput):
    """схема для создания запчасти"""
    name: str = Field(min_length=1, max_length=200)
    purpose: DronePurpose
    price: int = Field(gt=0)
    drone_id: UUID | None


class ReadPart(BaseOutput):
    """схема ответа запчасти"""
    id: UUID
    name: str
    purpose: DronePurpose
    price: int
    drone_id: UUID
    model_config = ConfigDict(from_attributes=True)


class UpdatePart(BaseInput):
    """схема изменения запчасти, все поля не обязательные"""
    name: str | None = Field(min_length=1, max_length=200, default=None)
    purpose: DronePurpose | None = None
    price: int | None = Field(gt=0, default=None)
    drone_id: UUID | None = None

    @field_validator("name", "purpose", "price")
    @classmethod
    def check_null(cls, value):
        if value is not None:
            return value
        return ValueError("значение не может быть null")


class PaginationPart(BaseInput):
    items: list[ReadPart]
    total: int
    limit: int
    offset: int

