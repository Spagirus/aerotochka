from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import get_session
from src.schemas.customer import ReadCustomer
from src.service.service_customer import ServiceCustomer

router = APIRouter(
    tags=["Customers"],
    prefix="/api/v1/customer"
)



@router.get("/{id}/")
async def get_customer(id:str, session: SessionDep, service: ServiceCustomer) -> ReadCustomer:
    result = await service(session=session).get_customer(customer_id=id)
    return result

