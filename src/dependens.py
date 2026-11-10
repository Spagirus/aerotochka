from src.service.service_customer import ServiceCustomer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db import get_session
from fastapi import Depends


SessionDep = Annotated[AsyncSession, Depends(get_session)]

