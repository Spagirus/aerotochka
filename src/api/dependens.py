from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import get_session
from src.application.services.service_customer import ServiceCustomer
from src.infra.repositories.customer import CustomerRepo

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_customer_service(session: SessionDep) -> ServiceCustomer:
    return ServiceCustomer(CustomerRepo(session))


customer_dep = Annotated[ServiceCustomer, Depends(get_customer_service)]
