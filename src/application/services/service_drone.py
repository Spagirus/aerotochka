from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.application.schemas.drone import CreateDrone, PurchaseDrone, UpdateDrone
from src.domain.enums import DroneStatus, LicenseStatus
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
        drone = await self.repo.search_by_id(drone_id)
        if not isinstance(drone, Drone):
            raise NotFound404Error(code="DRONE_NOT_FOUND",
                                   message=f"дрон с id ({drone_id}) не найден")
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
        drone = await self.repo.search_by_id(drone_id)
        if not isinstance(drone, Drone):
            raise NotFound404Error(code="DRONE_NOT_FOUND",
                                   message=f"дрон с id ({drone_id}) не найден")

        customer = await self.customer_repo.search_by_id(customer_id.customer_id)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с {customer_id} не найден")

        if drone.status != DroneStatus.IN_STOCK:
            raise Conflict409Error(code="DRONE_NOT_AVAILABLE",
                                   message="дрон уже куплен или снят с продажи")

        last_license = await self.license_repo.get_last_license_customer(customer_id.customer_id)
        if last_license is None or last_license.status == LicenseStatus.REVOKED:
            raise Conflict409Error(code="NO_LICENSE", message="У покупателя нет лицензии или последняя отозвана")
        if last_license.status == LicenseStatus.SUSPENDED:
            raise Conflict409Error(code="LICENSE_SUSPENDED", message="последняя лицензия приостановлена")
        now = get_msk_time()
        today = now.date()
        await self.license_repo.check_execute(today)
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
