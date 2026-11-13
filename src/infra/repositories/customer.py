from uuid import UUID
from src.infra.models.customer import Customer
from src.infra.models.license import License
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CustomerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self, customer_id: UUID) -> Customer | None:
        """поиск покупателя по айди"""
        return await self.session.get(Customer, customer_id)

    async def create_customer(self, customer) -> Customer:
        """создание покупателя"""
        self.session.add(customer)
        await self.session.commit()
        await self.session.refresh(customer)
        return customer

    async def update_customer(self, customer) -> Customer:
        """изменение покупателя"""
        await self.session.commit()
        await self.session.refresh(customer)
        return customer

    async def search_licenses_customer(self, customer_id: UUID) -> License:
        """поиск всех лицензий автора"""
        stmt = select(License).where(License.customer_id == customer_id)
        res = await self.session.scalar(stmt)
        return res
