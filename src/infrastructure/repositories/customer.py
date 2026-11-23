"""репозиторий покупателя (работа с бд)"""

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import FlightRank, LicenseStatus
from src.infrastructure.models.customer import Customer
from src.infrastructure.models.license import License


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

    async def get_rank_customer(self, customer_id: UUID, today: date) -> FlightRank | None:
        """вычисление ранга покупателя по его лицензии"""
        stmt = (select(License.rank).where(License.customer_id == customer_id,
                                           License.status == LicenseStatus.ACTIVE,
                                           License.valid_until >= today,
                                           ).order_by(License.issued_at.desc()).limit(1))
        return await self.session.scalar(stmt)

    async def get_customers(self, phone: str | None, limit: int, offset: int):
        """ получение списка покупателей пагинацией"""
        stmt = select(Customer)
        if phone is not None:
            stmt = stmt.where(Customer.phone == phone)
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = stmt.order_by(Customer.created_at.desc()).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all()), total

    async def get_licenses_pagination(self, customer_id: UUID, limit: int, offset: int):
        """получение списка лицензий покупателя пагинацией """
        stmt = select(License).where(License.customer_id == customer_id)
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = stmt.order_by(License.issued_at.desc()).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all()), total
