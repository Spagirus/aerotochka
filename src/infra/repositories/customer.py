from uuid import UUID
from src.infra.models.customer import Customer
from src.infra.models.license import License
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CustomerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self, customer_id: UUID) -> Customer | None:
        return await self.session.get(Customer, customer_id)

    async def create_customer(self, customer) -> Customer:
        self.session.add(customer)
        await self.session.commit()
        await self.session.refresh(customer)
        return customer

    async def update_customer(self, customer) -> Customer:
        await self.session.commit()
        await self.session.refresh(customer)
        return customer

    async def search_licenses_customer(self, customer_id: UUID):
        stmt = select(License).where(License.customer_id == customer_id)
        res = await self.session.scalars(stmt)
        return list(res.all())
