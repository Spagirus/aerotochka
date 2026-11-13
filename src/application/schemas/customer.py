"""схемы для покупателя"""

from datetime import date, datetime
from uuid import UUID

from pydantic import Field, field_validator, ConfigDict

from src.domain.enums import FlightRank
from src.application.schemas.base_schemas import BaseInput, BaseOutput


class CreateCustomer(BaseInput):
    full_name: str
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
    id: UUID
    full_name: str
    phone: str
    email: str = None
    birth_date: date
    rank: FlightRank | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateCustomer(BaseInput):
    full_name: str | None = None
    phone: str | None = Field(default = None, pattern=r'^+7\[0-9]{10}$')
    email: str | None = None
    birth_date: date | None = None

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date


