from uuid import UUID
from src.infra.models.customer import Customer
from src.infra.models.license import License
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class LicenseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self,license_id: UUID) -> License | None:
        return await self.session.get(License, license_id)

    async def create_license(self, license) -> License:
        self.session.add(license)
        await self.session.commit()
        await self.session.refresh(license)
        return license

