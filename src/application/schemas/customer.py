"""схемы для покупателя"""

from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from src.application.schemas.base_schemas import BaseInput, BaseOutput
from src.domain.enums import FlightRank


class CreateCustomer(BaseInput):
    """схема для создания покупателя, проверяет на актуальную дату"""
    full_name: str = Field(min_length=1)
    phone: str = Field(pattern=r'^\+7[0-9]{10}$')
    email: EmailStr | None = None
    birth_date: date

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date

    @field_validator("full_name")
    @classmethod
    def valid_full_name(cls, full_name: str):
        if full_name.strip().count(" ") != 2:
            raise ValueError("должно быть полное ФИО")
        return full_name


class ReadCustomer(BaseOutput):
    """схема ответа покупателя"""
    id: UUID
    full_name: str
    phone: str
    email: EmailStr | None = None
    birth_date: date
    rank: FlightRank | None = None
    created_at: datetime



class UpdateCustomer(BaseInput):
    """схема ответа покупателя, все поля не обязательные"""
    full_name: str | None = None
    phone: str | None = Field(default=None, pattern=r'^\+7[0-9]{10}$', examples=["+79503098420"])
    email: EmailStr | None = None
    birth_date: date | None = None

    @field_validator("birth_date")
    @classmethod
    def valid_date(cls, b_date: date):
        """проверка на актуальное время"""
        if b_date is not None and b_date > date.today():
            raise ValueError("введённая дата находится в будущем")
        return b_date

    @field_validator("full_name")
    @classmethod
    def valid_full_name(cls, full_name: str):
        if full_name is not None and full_name.strip().count(" ") != 2:
            raise ValueError("должно быть полное ФИО")
        return full_name


class PaginationCustomer(BaseInput):
    """схема пагинации"""
    items: list[ReadCustomer]
    total: int
    limit: int
    offset: int


