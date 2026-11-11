"""модуль с Сервисом покупателя, бизнес-правила и т.д"""

from uuid import UUID

from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.exceptions import Conflict409Error, NotFound404Error
from src.infra.db import AsyncSession
from src.infra.models import Customer, License
from src.schemas.customer import CreateCustomer, UpdateCustomer


class ServiceCustomer:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_customer(self, customer_id: UUID) -> Customer:
        """поиск покупателя по айди"""
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = await self.session.scalar(stmt)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с id ({customer_id}) не найден")
        return customer

    async def add_customer(self, data: CreateCustomer) -> Customer:
        """добавление покупателя, возвращает объект"""
        customer = Customer(**data.model_dump())
        self.session.add(customer)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Conflict409Error(code="PHONE_ALREADY_EXISTS",
                                   message=f"Покупатель с таким телефоном"
                                           f"({customer.phone}) уже есть") from None
        return customer

    async def update_customer(self, customer_id: UUID, data: UpdateCustomer) -> Customer:
        """изменение покупателя, проверка на совершеннолетие"""
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = await self.session.scalar(stmt)
        if not isinstance(customer, Customer):
            raise NotFound404Error(code="CUSTOMER_NOT_FOUND",
                                   message=f"покупатель с id ({customer_id} не найден") from None
        modification = data.model_dump(exclude_unset=True)

        if "birth_date" in modification:
            birth_date = modification["birth_date"]
            stmt = select(License).where(License.customer_id == customer_id)
            all_issued = (await self.session.scalar(stmt)).all()

            for issue in all_issued:
                difference = relativedelta(issue.date(), birth_date)
                if difference.years < 18:
                    raise Conflict409Error(code="CUSTOMER_UNDERAGE",
                                           message="Вам должно быть 18"
                                                   " на момент выдачи лицензии!")

        for key, value in modification.items():
            setattr(customer, key, value)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Conflict409Error(
                code="PHONE_ALREADY_EXISTS",
                message=f"Покупатель с телефоном {customer.phone} уже есть",
            ) from None

        return customer








