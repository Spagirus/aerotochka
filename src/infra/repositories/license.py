"""репозиторий лицензии (работа с бд)"""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import LicenseStatus
from src.infra.models.license import License


class LicenseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_execute(self, day: date):
        """проверка актуальности лицензии, вызывается каждый раз"""
        stmt = (
            update(License)
            .where(
                or_(License.status == LicenseStatus.ACTIVE, License.status == LicenseStatus.SUSPENDED),
                License.valid_until < day,
            )
            .values(status=LicenseStatus.EXPIRED)
        )

        await self.session.execute(stmt)
        await self.session.commit()

    async def search_by_id(self,license_id: UUID) -> License | None:
        """поиск по айди лицензии"""
        return await self.session.get(License, license_id)

    async def create_license(self, license) -> License:
        """создание лицензии"""
        self.session.add(license)
        await self.session.commit()
        await self.session.refresh(license)
        return license

    async def search_by_customer(self, customer_id: UUID) -> list[License]:
        """ищет все лицензии покупателя по его айди"""
        stmt = select(License).where(License.customer_id == customer_id)
        res = await self.session.scalars(stmt)
        return list(res.all())

    async def get_active_customer_id(self, customer_id: UUID, date: datetime) -> License:
        """ищет действующую лицензию покупателя по его айди"""
        stmt = select(License).where(License.customer_id == customer_id,
                                     License.status == LicenseStatus.ACTIVE,
                                     License.valid_until > date)
        return await self.session.scalar(stmt)

    async def update_license(self, license) -> License:
        """изменение лицензии"""
        await self.session.commit()
        await self.session.refresh(license)
        return license

    async def check_limit(self, start_day: datetime, end_day: datetime)-> int:
        """проверка лимита 3 в день"""
        stmt = select(func.count(License.id)).where(License.issued_at >= start_day,
                                     License.issued_at < end_day)
        res = await self.session.scalar(stmt)
        return res or 0

