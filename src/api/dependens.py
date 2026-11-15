"""зависимости"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.service_customer import ServiceCustomer
from src.application.services.service_license import ServiceLicense
from src.infra.db import get_session
from src.infra.repositories.customer import CustomerRepo
from src.infra.repositories.license import LicenseRepo

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_customer_service(session: SessionDep) -> ServiceCustomer:
    return ServiceCustomer(CustomerRepo(session))

def get_license_service(session: SessionDep) -> ServiceLicense:
    return ServiceLicense(LicenseRepo(session),CustomerRepo(session))

customer_dep = Annotated[ServiceCustomer, Depends(get_customer_service)]
license_dep = Annotated[ServiceLicense, Depends(get_license_service)]
