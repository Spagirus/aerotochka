from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.drone  import Drone
from src.infra.models.part import Part


class DroneRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self, drone_id: UUID) -> Drone  | None:
        """поиск дрона по айди"""
        return await self.session.get(Drone , drone_id)

    async def create_drone(self, drone) -> Drone :
        """создание дрона"""
        self.session.add(drone)
        await self.session.commit()
        await self.session.refresh(drone)
        return drone

    async def update_drone (self, drone) -> Drone:
        """изменение дрона"""
        await self.session.commit()
        await self.session.refresh(drone)
        return drone

    async def search_parts_drone(self, drone_id: UUID) -> list[Part | None] | None:
        """поиск всех запчастей дрона"""
        stmt = select(Part).where(Part.drone_id == drone_id)
        result = await self.session.scalars(stmt)
        return list(result.all())