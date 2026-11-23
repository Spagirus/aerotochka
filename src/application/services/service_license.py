"""сервис Лицензии, бизнес правила, проверки и т.д"""
from uuid import UUID

from dateutil.relativedelta import relativedelta

from src.application.schemas.license import CreateLicense, RevokeBody
from src.domain.enums import LicenseStatus
from src.domain.exceptions import Conflict409Error, NotFound404Error
from src.infrastructure.models import Customer, License
from src.infrastructure.models.utils import get_msk_time
from src.infrastructure.repositories.customer import CustomerRepo
from src.infrastructure.repositories.license import LicenseRepo


class ServiceLicense:
    def __init__(self, repo: LicenseRepo, customer_repo: CustomerRepo):
        self.repo = repo
        self.customer_repo = customer_repo

    async def get_license(self, license_id) -> License:
        """получение лицензии через её id"""
        today = get_msk_time()
        await self.repo.check_execute(today.date())
        license = await self.repo.search_by_id(license_id)
        if not isinstance(license, License):
            raise NotFound404Error(code="LICENSE_NOT_FOUND",
                                   message=f"лицензия с id ({license_id}) не найдена")
        return license

    async def create_license(self, data: CreateLicense) -> License:
        """
        создание / повышение лицензии,
        проверка лимита 3 в день,
        совершеннолетие покупателя,
        проверка на наличие других действующих выше или того же ранга лицензий
        """
        now = get_msk_time()
        today = now.date()
        await self.repo.check_execute(today)
        customer = await self.customer_repo.search_by_id(data.customer_id)
        if not isinstance(customer, Customer):
            raise NotFound404Error(
                code="CUSTOMER_NOT_FOUND", message=f"покупатель с id ({data.customer_id}) не найден"
            )

        if relativedelta(today, customer.birth_date).years < 18:
            raise Conflict409Error(code="CUSTOMER_UNDERAGE",
                                   message="покупателю нет 18 лет на дату выдачи")

        start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = start_day + relativedelta(days=1)
        if await self.repo.check_limit(start_day, end_day) >= 3:
            raise Conflict409Error(code="DAILY_LIMIT_REACHED",
                                   message="за сегодняшний день (по Москве)"
                                           " уже выдано 3 лицензии")

        active = await self.repo.get_active_customer_id(data.customer_id, today)
        if active:
            if active.rank.rank >= data.rank.rank:
                raise Conflict409Error(
                    code="ACTIVE_LICENSE_EXISTS",
                 message="уже есть действующая лицензия того же или более высокого ранга",
                )

            active.status = LicenseStatus.REVOKED
            active.revoke_reason = "заменена новой лицензией"
        return await self.repo.create_license(License(**data.model_dump()))

    async def suspend_license(self, license_id: UUID) -> License:
        """приостановка лицензии, проверка что лицензия активна"""
        today = get_msk_time()
        await self.repo.check_execute(today.date())
        license = await self.get_license(license_id)

        if license.status != LicenseStatus.ACTIVE:
            raise Conflict409Error(code="INVALID_LICENSE_TRANSITION", message="лицензия не активна")
        license.status = LicenseStatus.SUSPENDED
        return await self.repo.update_license(license)

    async def resume_license(self, license_id: UUID) -> License:
        """
        возобновление приостановленной лицензии,
        проверяет что лицензия приостановлена или уже истекла
        """
        today = get_msk_time()
        await self.repo.check_execute(today.date())
        license = await self.get_license(license_id)
        if license.status != LicenseStatus.SUSPENDED or license.valid_until < today.date():
            raise Conflict409Error(code="INVALID_LICENSE_TRANSITION",
                                   message="лицензия не приостановлена или просрочена")
        license.status = LicenseStatus.ACTIVE
        return await self.repo.update_license(license)

    async def revoke_license(self, license_id: UUID, revoke: RevokeBody) -> License:
        """отзыв лицензии, принимает причину, проверка что лицензия уже не отозвана"""
        today = get_msk_time()
        await self.repo.check_execute(today.date())
        license = await self.get_license(license_id)
        if license.status in (LicenseStatus.REVOKED, LicenseStatus.EXPIRED):
            raise Conflict409Error(code="INVALID_LICENSE_TRANSITION",
                                   message="лицензия уже отозвана или истекла")
        license.status = LicenseStatus.REVOKED
        license.revoke_reason = revoke.reason

        return await self.repo.update_license(license)

    async def get_licenses(
            self,
            limit: int,
            offset: int,
            key: str | None,
            customer_id: UUID | None,
            status: LicenseStatus | None
    ) -> dict:
        """пагинация лицензии"""
        await self.repo.check_execute(get_msk_time().date())
        items, total = await self.repo.get_licenses(
            limit=limit,
            offset=offset,
            key=key,
            customer_id=customer_id,
            status=status
        )
        return {"items": items, "total": total, "limit": limit, "offset": offset}

    async def renewal_license(self, license_id: UUID) -> License:
        """
        продение лицензии на 1 год, продлить можно только активную,
        которой осталось 3 месяца до истечения,
        чтобы нельзя было продлить разам на больше лет просто потыкав кнопку
        """
        today = get_msk_time().date()
        await self.repo.check_execute(today)
        license = await self.get_license(license_id)
        if license.status != LicenseStatus.ACTIVE or license.valid_until < today:
            raise Conflict409Error(
                code="INVALID_LICENSE_RENEWAL",
                message="лицензия должна быть активна для продления"
            )

        if license.valid_until > today + relativedelta(months=3):
            raise Conflict409Error(
                code="INVALID_LICENSE_RENEWAL",
                message="лицензию можно продлить только раз в 9 месяцев"
            )
        license.valid_until += relativedelta(years=1)
        return await self.repo.update_license(license)
