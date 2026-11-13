from uuid import UUID
from src.infra.models.license import License
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from src.domain.enums import LicenseStatus
class LicenseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

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
        await self.session.commit()
        await self.session.refresh(license)
        return license