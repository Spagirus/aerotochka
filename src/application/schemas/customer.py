"""схемы для покупателя"""

from datetime import date, datetime
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator

from src.application.schemas.base_schemas import BaseInput, BaseOutput
from src.domain.enums import FlightRank


class CreateCustomer(BaseInput):
    """схема для создания покупателя, проверяет на актуальную дату"""
    full_name: str = Field(min_length=1)
    phone: str = Field(pattern=r'^\+7[0-9]{10}$')
    email: str | None = None  # если время будет, добавь проверку почты
    birth_date: date

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date


class ReadCustomer(BaseOutput):
    """схема ответа покупателя"""
    id: UUID
    full_name: str
    phone: str
    email: str | None = None
    birth_date: date
    rank: FlightRank | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateCustomer(BaseInput):
    """схема ответа покупателя, все поля не обязательные"""
    full_name: str | None = None
    phone: str | None = Field(default=None, pattern=r'^\+7[0-9]{10}$', examples=["+79503098420"])
    email: str | None = None
    birth_date: date | None = None

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date is not None and b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date


class PaginationCustomer(BaseInput):
    """схема пагинации"""
    items: list[ReadCustomer]
    total: int
    limit: int
    offset: int


