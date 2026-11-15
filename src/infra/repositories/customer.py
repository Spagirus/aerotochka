"""репозиторий покупателя (работа с бд)"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.customer import Customer
from src.infra.models.license import License


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

    async def search_licenses_customer(self, customer_id: UUID) -> list[License]:
        """поиск всех лицензий автора"""
        stmt = select(License).where(License.customer_id == customer_id)
        result = await self.session.scalars(stmt)
        return list(result.all())
