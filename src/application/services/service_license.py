from src.infra.repositories.license import LicenseRepo
from src.infra.models import License
from src.application.schemas.license import CreateLicense
from src.domain.exceptions import NotFound404Error
from src.infra.repositories.customer import CustomerRepo

class ServiceLicense:
    def __init__(self, repo: LicenseRepo, customer_repo: CustomerRepo):
        self.repo = repo
        self.customer_repo = customer_repo

    async def get_license(self, license_id) -> License:
        license = await self.repo.search_by_id(license_id)
        if not isinstance(license, License):
            raise NotFound404Error(code="LICENSE_NOT_FOUND",
                                   message=f"покупатель с id ({license}) не найден")
        return license

    async def create_license(self, data: CreateLicense) -> License:
        new_license = License(**data.model_dump())
        license_customer = await self.repo.search_by_customer(new_license.customer_id)



