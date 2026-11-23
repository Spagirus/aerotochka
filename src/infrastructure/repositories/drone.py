from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums import DronePurpose, DroneStatus, FlightRank
from src.infrastructure.models.drone import Drone
from src.infrastructure.models.part import Part


class DroneRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_by_id(self, drone_id: UUID) -> Drone | None:
        """поиск дрона по айди"""
        return await self.session.get(Drone, drone_id)

    async def create_drone(self, drone) -> Drone:
        """создание дрона"""
        self.session.add(drone)
        await self.session.commit()
        await self.session.refresh(drone)
        return drone

    async def update_drone(self, drone) -> Drone:
        """изменение дрона"""
        await self.session.commit()
        await self.session.refresh(drone)
        return drone

    async def search_parts_drone(self, drone_id: UUID, limit: int, offset: int):
        """поиск всех запчастей дрона"""
        stmt = select(Part).where(Part.drone_id == drone_id)
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        stmt = stmt.order_by(Part.price.desc()).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all()), total

    async def get_parts_drone(self, drone_id: UUID) -> list[Part]:
        """все запчасти дрона списком(не пагинацией!!)"""
        stmt = select(Part).where(Part.drone_id == drone_id)
        return list((await self.session.scalars(stmt)).all())

    async def get_drones(
            self,
            limit: int,
            offset: int,
            purpose: DronePurpose | None,
            rank: FlightRank | None,
            max_rank: FlightRank | None,
            status: DroneStatus | None,
            manufacturer: str | None,
            has_camera: bool | None,
            min_price: int | None,
            max_price: int | None,
            customer_id: UUID | None
            ):
        """получение спика дронов пагинацией с кучей фильтров"""
        stmt = select(Drone)
        if purpose is not None:
            stmt = stmt.where(Drone.purpose == purpose)
        if rank is not None:
            stmt = stmt.where(Drone.rank == rank)
        if max_rank is not None:
            ranks = [rankk for rankk in FlightRank if rankk.rank <= max_rank.rank]
            stmt = stmt.where(Drone.rank.in_(ranks))
        if status is not None:
            stmt = stmt.where(Drone.status == status)
        if manufacturer is not None:
            stmt = stmt.where(func.lower(Drone.manufacturer) == manufacturer.strip().lower())
        if has_camera is not None:
            stmt = stmt.where(Drone.has_camera == has_camera)
        if min_price is not None:
            stmt = stmt.where(Drone.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Drone.price <= max_price)
        if customer_id is not None:
            stmt = stmt.where(Drone.customer_id == customer_id)
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        stmt = stmt.order_by(Drone.created_at.desc()).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all()), total
