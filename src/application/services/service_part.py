"""модуль с Сервисом покупателя, бизнес-правила и т.д"""

from uuid import UUID

from src.application.schemas.part import CreatePart, UpdatePart
from src.domain.enums import DronePurpose
from src.domain.exceptions import Conflict409Error, NotFound404Error
from src.infra.models import Part
from src.infra.models.drone import Drone
from src.infra.repositories.drone import DroneRepo
from src.infra.repositories.part import PartRepo


class ServicePart:
    def __init__(self, repo: PartRepo, drone_repo: DroneRepo):
        self.repo = repo
        self.drone_repo = drone_repo

    async def get_part(self, part_id: UUID) -> Part:
        """поиск запчасти по айди"""
        part = await self.repo.search_by_id(part_id)
        if not isinstance(part, Part):
            raise NotFound404Error(code="PART_NOT_FOUND",
                                   message=f"запчасть с id ({part_id}) не найден")
        return part

    async def add_part(self, data: CreatePart) -> Part:
        """добавление запчасти, возвращает объект"""
        part = Part(**data.model_dump())
        if data.drone_id is not None:
            drone = await self.get_part(data.drone_id)
            if part.purpose != drone.purpose:
                raise Conflict409Error(
                    code="PART_PURPOSE_MISMATCH",
                    message='тип запчасти не совпадает с типом дрона'
                )

        return await self.repo.create_part(part)

    async def update_part(self, part_id: UUID, data: UpdatePart) -> Part:
        """изменение запчасти"""
        part = await self.get_part(part_id)

        modification = data.model_dump(exclude_unset=True)

        if "drone_id" in modification:
            drone_id = modification["drone_id"]
            if part.drone_id is not None and drone_id is not None:
                raise Conflict409Error(
                    code="PART_ALREADY_ATTACHED",
                    message="запчасть уже привязана к другому дрону."
                )

        new_drone_id = modification.get("drone_id", part.drone_id)
        new_purpose = modification.get("purpose", part.purpose)
        if new_drone_id:
            drone = await self.drone_repo.search_by_id(new_drone_id)
            if not isinstance(drone, Drone):
                raise NotFound404Error(code="DRONE_NOT_FOUND",
                                       message=f"дрон с id ({data.drone_id}) не найден")
            if drone.purpose != new_purpose:
                raise Conflict409Error(
                    code="PART_PURPOSE_MISMATCH",
                    message='тип запчасти не совпадает с типом дрона'
                )

        for key, value in modification.items():
            setattr(part, key, value)

        return await self.repo.update_part(part)

    async def delete_part(self, part_id: UUID) -> None:
        """удаление запчасти"""
        part = await self.get_part(part_id)
        await self.repo.delete_part(part)

    async def get_parts(
            self,
            purpose: DronePurpose | None,
            attached: bool | None,
            limit: int,
            offset: int
            ):
        """пагинация запчастей"""
        items, total = await self.repo.get_parts(
            purpose=purpose,
            attached=attached,
            limit=limit,
            offset=offset
        )
        return {"items": items, "total": total, "limit": limit, "offset": offset}
