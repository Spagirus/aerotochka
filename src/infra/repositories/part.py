"""репозиторий запчасти (работа с бд)"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.part import Part


class PartRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self, part_id: UUID) -> Part | None:
        """поиск запчасти по айди"""
        return await self.session.get(Part, part_id)

    async def create_part(self, part) -> Part:
        """создание запчасти"""
        self.session.add(part)
        await self.session.commit()
        await self.session.refresh(part)
        return part

    async def update_part(self, part) -> Part:
        """изменение запчасти"""
        await self.session.commit()
        await self.session.refresh(part)
        return part
