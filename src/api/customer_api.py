"""ендпоинты покупателя"""
from uuid import UUID

from fastapi import APIRouter

from src.api.dependens import customer_dep
from src.application.schemas.customer import CreateCustomer, ReadCustomer, UpdateCustomer

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



