"""модуль с Сервисом покупателя, бизнес-правила и т.д"""

from uuid import UUID

from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError

from src.application.schemas.customer import CreateCustomer, UpdateCustomer
from src.domain.exceptions import Conflict409Error, NotFound404Error
from src.infra.models import Customer
from src.infra.models.utils import get_msk_time
from src.infra.repositories.customer import CustomerRepo


class ServiceCustomer:
    def __init__(self, repo: CustomerRepo):
        self.repo = repo

    async def get_customer(self, customer_id: UUID) -> Customer:
        """поиск покупателя по айди"""
        customer = await self.repo.search_by_id(customer_id)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с id ({customer_id}) не найден")
        today = get_msk_time().date()
        customer.rank = await self.repo.get_rank_customer(customer_id, today)
        return customer

    async def add_customer(self, data: CreateCustomer) -> Customer:
        """добавление покупателя, возвращает объект"""
        customer = Customer(**data.model_dump())
        try:
            await self.repo.create_customer(customer)
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(code="PHONE_ALREADY_EXISTS",
                                   message=f"Покупатель с таким телефоном"
                                           f"({customer.phone}) уже есть") from None
        customer.rank = None
        return customer

    async def update_customer(self, customer_id: UUID, data: UpdateCustomer) -> Customer:
        """изменение покупателя, проверка на совершеннолетие"""
        customer = await self.get_customer(customer_id)

        modification = data.model_dump(exclude_unset=True, exclude_none=True)

        if "birth_date" in modification:
            birth_date = modification["birth_date"]
            all_issued = await self.repo.search_licenses_customer(customer_id)
            for issue in all_issued:
                difference = relativedelta(issue.issued_at, birth_date)
                if difference.years < 18:
                    raise Conflict409Error(code="CUSTOMER_UNDERAGE",
                                           message="Вам должно быть 18"
                                                   " на момент выдачи лицензии!")

        for key, value in modification.items():
            setattr(customer, key, value)

        try:
            await self.repo.update_customer(customer)
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(
                code="PHONE_ALREADY_EXISTS",
                message=f"Покупатель с телефоном {customer.phone} уже есть",
            ) from None
        customer.rank = None
        return customer

    async def pagination_customer(self, limit: int, offset: int, phone: str | None) -> dict:
        """пагинация покупателя с выдачей каждому ранга по его лицензии"""
        items, total = await self.repo.get_customers(limit=limit, offset=offset, phone=phone)
        today = get_msk_time().date()
        for customer in items:
            customer.rank = await self.repo.get_rank_customer(customer.id, today)

        return {"items": items, "total": total, "limit": limit, "offset": offset}

    async def get_licenses_customer(self, customer_id: UUID, limit: int, offset: int) -> dict:
        """пагинация получения всех лицензий покупателя"""
        items, total = await self.repo.get_licenses_pagination(
            limit=limit,
            offset=offset,
            customer_id=customer_id
        )
        return {"items": items, "total": total, "limit": limit, "offset": offset}
