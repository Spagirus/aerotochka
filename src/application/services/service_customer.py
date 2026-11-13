"""модуль с Сервисом покупателя, бизнес-правила и т.д"""

from uuid import UUID

from dateutil.relativedelta import relativedelta

from sqlalchemy.exc import IntegrityError

from src.domain.exceptions import Conflict409Error, NotFound404Error
from src.infra.models import Customer
from src.application.schemas.customer import CreateCustomer, UpdateCustomer
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
        return customer

    async def add_customer(self, data: CreateCustomer) -> Customer:
        """добавление покупателя, возвращает объект"""
        customer = Customer(**data.model_dump())
        await self.repo.create_customer(customer)
        try:
            await self.repo.create_customer(customer)
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(code="PHONE_ALREADY_EXISTS",
                                   message=f"Покупатель с таким телефоном"
                                           f"({customer.phone}) уже есть") from None
        return customer

    async def update_customer(self, customer_id: UUID, data: UpdateCustomer) -> Customer:
        """изменение покупателя, проверка на совершеннолетие"""
        customer = await self.repo.search_by_id(customer_id)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с id ({customer_id} не найден") from None
        modification = data.model_dump(exclude_unset=True)

        if "birth_date" in modification:
            birth_date = modification["birth_date"]
            all_issued = await self.repo.search_licenses_customer(customer_id)
            for issue in all_issued:
                difference = relativedelta(issue.date(), birth_date)
                if difference.years < 18:
                    raise Conflict409Error(code="CUSTOMER_UNDERAGE",
                                           message="Вам должно быть 18"
                                                   " на момент выдачи лицензии!")


        for key, value in modification.items():
            setattr(customer, key, value)

        try:
            await self.repo.session.commit()
        except IntegrityError:
            await self.repo.session.rollback()
            raise Conflict409Error(
                code="PHONE_ALREADY_EXISTS",
                message=f"Покупатель с телефоном {customer.phone} уже есть",
            ) from None

        return customer








