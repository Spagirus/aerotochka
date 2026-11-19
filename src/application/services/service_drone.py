from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.application.schemas.drone import CreateDrone, FlightRank, PurchaseDrone, UpdateDrone
from src.domain.enums import DronePurpose, DroneStatus, LicenseStatus
from src.domain.exceptions import Conflict409Error, NotFound404Error
from src.infra.models import Drone
from src.infra.models.customer import Customer
from src.infra.models.drone import get_msk_time
from src.infra.repositories.customer import CustomerRepo
from src.infra.repositories.drone import DroneRepo
from src.infra.repositories.license import LicenseRepo


class ServiceDrone:
    def __init__(self, repo: DroneRepo, customer_repo: CustomerRepo, license_repo: LicenseRepo):
        self.repo = repo
        self.customer_repo = customer_repo
        self.license_repo = license_repo

    async def get_drone(self, drone_id: UUID) -> Drone:
        """поиск дрона по айди"""
        drone = await self.repo.search_by_id(drone_id)
        if not isinstance(drone, Drone):
            raise NotFound404Error(code="DRONE_NOT_FOUND",
                                   message=f"дрон с id ({drone_id}) не найден")
        return drone

    async def add_drone(self, data: CreateDrone) -> Drone:
        """добавление дрона, возвращает объект"""
        drone = Drone(**data.model_dump())
        try:
            await self.repo.create_drone(drone)
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(code="SKU_ALREADY_EXISTS",
                                   message=f"Дрон с таким sku"
                                           f"({drone.sku}) уже есть") from None
        return drone

    async def update_drone(self, data: UpdateDrone, drone_id: UUID) -> Drone:
        """изменение дрона"""
        drone = await self.get_drone(drone_id)

        if drone.status == DroneStatus.SOLD:
            raise Conflict409Error(code="DRONE_SOLD", message="дрон уже продан")

        modification = data.model_dump(exclude_unset=True, exclude_none=True)
        if "status" in modification and modification["status"] == DroneStatus.SOLD:
            raise Conflict409Error(
                code="INVALID_DRONE_STATUS",
                message="нельзя перевести в sold - продажа идёт только через покупку"
            )

        for key, value in modification.items():
            setattr(drone, key, value)
        drone.updated_at = get_msk_time()

        try:
            await self.repo.update_drone(drone)
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(
                code="SKU_ALREADY_EXISTS",
                message=f"дрон с sku ({drone.sku}) уже есть",
            ) from None

        return drone

    async def purchase_drone(self, customer_id: PurchaseDrone, drone_id: UUID) -> Drone:
        """покупка дрона"""
        drone = await self.get_drone(drone_id)

        customer = await self.customer_repo.search_by_id(customer_id.customer_id)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с {customer_id} не найден")

        if drone.status != DroneStatus.IN_STOCK:
            raise Conflict409Error(code="DRONE_NOT_AVAILABLE",
                                   message="дрон уже куплен или снят с продажи")

        last_license = await self.license_repo.get_last_license_customer(customer_id.customer_id)
        if last_license is None or last_license.status == LicenseStatus.REVOKED:
            raise Conflict409Error(
                code="NO_LICENSE",
                message="У покупателя нет лицензии или последняя отозвана"
            )
        now = get_msk_time()
        today = now.date()
        await self.license_repo.check_execute(today)
        if last_license.status == LicenseStatus.SUSPENDED:
            raise Conflict409Error(code="LICENSE_SUSPENDED", message="последняя лицензия приостановлена")
        if last_license.status == LicenseStatus.EXPIRED:
            raise Conflict409Error(code="LICENSE_EXPIRED", message="последняя лицензия истекла")
        if last_license.rank.rank < drone.rank.rank:
            raise Conflict409Error(
                code="LICENSE_RANK_TOO_LOW",
                message=f"Для дрона ранга {drone.rank} нужна лицензия ранга {drone.rank} или выше,"
                        f" у покупателя — {last_license.rank}"
            )
        drone.status = DroneStatus.SOLD
        drone.customer_id = customer.id
        drone.sold_at = now
        drone.sold_price = drone.price
        drone.sold_license_id = last_license.id

        return await self.repo.update_drone(drone)

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
            ) -> dict:
        """пагинация дрона"""
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(status_code=422, detail="минимальная цена не может быть больше максимальной")
        items, total = await self.repo.get_drones(
            limit=limit,
            offset=offset,
            purpose=purpose,
            rank=rank,
            max_rank=max_rank,
            status=status,
            manufacturer=manufacturer,
            has_camera=has_camera,
            customer_id=customer_id,
            min_price=min_price,
            max_price=max_price)
        return {"items": items, "total": total, "limit": limit, "offset": offset}

    async def get_parts_drone(self, drone_id: UUID, limit: int, offset: int) -> dict:
        items, total = await self.repo.search_parts_drone(limit=limit, offset=offset, drone_id=drone_id)
        return {"items": items, "total": total, "limit": limit, "offset": offset}
