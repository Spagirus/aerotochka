"""репозиторий запчасти (работа с бд)"""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import DronePurpose
from src.infrastructure.models.part import Part


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

    async def delete_part(self, part) -> None:
        """удаление запчасти"""
        await self.session.delete(part)
        await self.session.commit()

    async def get_parts(
            self,
            purpose: DronePurpose | None,
            attached: bool | None,
            limit: int,
            offset: int
    ):
        """получение всех запчастей"""
        stmt = select(Part)
        if purpose is not None:
            stmt = stmt.where(Part.purpose == purpose)
        if attached is True:
            stmt = stmt.where(Part.drone_id.is_not(None))
        if attached is False:
            stmt = stmt.where(Part.drone_id.is_(None))
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        stmt = stmt.order_by(Part.price.desc()).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all()), total
