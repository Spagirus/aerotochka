"""схемы для покупателя"""

from datetime import date, datetime
from uuid import UUID

from pydantic import Field, field_validator

from src.enums import FlightRank
from src.schemas.base_schemas import BaseInput, BaseOutput


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
    email: str
    birth_date: str
    rank: FlightRank
    created_at: datetime


class UpdateCustomer(BaseInput):
    full_name: str | None
    phone: str | None = Field(pattern=r'^+7\[0-9]{10}$')
    email: str | None
    birth_date: date | None

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date


