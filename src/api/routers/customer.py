"""ендпоинты покупателя"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependens import customer_dep
from src.application.schemas.customer import CreateCustomer, PaginationCustomer, ReadCustomer, UpdateCustomer
from src.application.schemas.license import PaginationLicense

router = APIRouter(
    tags=["Customers"],
    prefix="/api/v1/customers"
)


@router.get("/{customer_id}")
async def get_customer(customer_id: UUID, service: customer_dep) -> ReadCustomer:
    """ручка получения покупателя по id"""
    return await service.get_customer(customer_id=customer_id)


@router.post("", status_code=201)
async def add_customer(data: CreateCustomer, service: customer_dep) -> ReadCustomer:
    """ручка добавления покупателя"""
    return await service.add_customer(data)


@router.patch("/{customer_id}")
async def patch_customer(customer_id: UUID, service: customer_dep, data: UpdateCustomer) -> ReadCustomer:
    """ручка изменения покупателя"""
    return await service.update_customer(customer_id=customer_id, data=data)

@router.get("")
async def get_customers(
        service: customer_dep,
        phone: str | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        ) -> PaginationCustomer:
    """ручка получения всех покупателей в формате пагинацией с фильтром по id"""
    return await service.pagination_customer(phone=phone, limit=limit, offset=offset)


@router.get("/{customer_id}/licenses")
async def get_licenses_customer(
        customer_id: UUID,
        service: customer_dep,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
) -> PaginationLicense:
    """ручка получения всех лицензий автора в формате пагинации"""
    return await service.get_licenses_customer(customer_id=customer_id, limit=limit, offset=offset)
