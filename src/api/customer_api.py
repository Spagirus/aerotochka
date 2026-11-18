"""ендпоинты покупателя"""
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependens import customer_dep
from src.application.schemas.customer import CreateCustomer, ReadCustomer, UpdateCustomer, PaginationCustomer
from typing import Annotated
router = APIRouter(
    tags=["Customers"],
    prefix="/api/v1/customers"
)


@router.get("/{id}")
async def get_customer(customer_id: UUID, service: customer_dep) -> ReadCustomer:
    return await service.get_customer(customer_id=customer_id)


@router.post("/", status_code=201)
async def add_customer(data: CreateCustomer, service: customer_dep) -> ReadCustomer:
    return await service.add_customer(data)


@router.patch("/{customer_id}")
async def patch_customer(customer_id: UUID, service: customer_dep, data: UpdateCustomer) -> ReadCustomer:
    return await service.update_customer(customer_id=customer_id, data=data)
@router.get("/")
async def get_customers(
        service: customer_dep,
        phone: str | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        ) -> PaginationCustomer:
    return await service.pagination_customer(phone=phone, limit=limit, offset=offset)

