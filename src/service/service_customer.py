from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from src.exceptions import Conflict409Error, NotFound404Error
from src.infra.db import AsyncSession
from src.infra.models.customer import Customer
from src.infra.models.license import License
from src.schemas.customer import CreateCustomer, UpdateCustomer


class ServiceCustomer:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_customer(self, data: CreateCustomer) -> Customer:
        customer = Customer(**data.model_dump())
        self.session.add(customer)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Conflict409Error(code="PHONE_ALREADY_EXISTS",
                                   message=f"Покупатель с таким телефоном"
                                           f"({customer.phone}) уже есть") from None
        return customer

    async def update_customer(self, customer_id: UUID, data: UpdateCustomer) -> Customer:
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = await self.session.scalar(stmt)
        if customer is None:
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с id ({customer_id} не найден")
        modification = data.model_dump(exclude_unset=True)

        if "birth_date" in modification:
            birth_date = modification["birth_date"]
            stmt = select(License).where(License.customer_id == customer_id)

        for key, value in modification.items():
            setattr(customer, key, value)
        await self.session.commit()
        return customer







