"""ендпоинты лицензии"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependens import license_dep
from src.application.schemas.license import CreateLicense, PaginationLicense, ReadLicense, RevokeBody
from src.domain.enums import LicenseStatus

router = APIRouter(
    tags=["Licenses"],
    prefix="/api/v1/licenses"
)


@router.get("/{license_id}")
async def get_license(license_id: UUID, service: license_dep) -> ReadLicense:
    """ручка получения лицензии по айди"""
    return await service.get_license(license_id=license_id)


@router.post("", status_code=201)
async def add_license(data: CreateLicense, service: license_dep) -> ReadLicense:
    """ручка создания лицензии"""
    return await service.create_license(data)


@router.post("/{license_id}/suspend", status_code=200)
async def suspend_license(license_id: UUID, service: license_dep) -> ReadLicense:
    """рчка приостоновки лицензии"""
    return await service.suspend_license(license_id)


@router.post("/{license_id}/renewal")
async def renewal_license_for_one_year(service: license_dep, license_id: UUID) -> ReadLicense:
    """ручка продления лицензии"""
    return await service.renewal_license(license_id)


@router.post("/{license_id}/resume", status_code=200)
async def resume_license(license_id: UUID, service: license_dep) -> ReadLicense:
    """ручка восстановления лицензии"""
    return await service.resume_license(license_id)


@router.post("/{id}/revoke", status_code=200)
async def revoke_license(license_id: UUID, service: license_dep, data: RevokeBody) -> ReadLicense:
    """ручка отзыва лицензии"""
    return await service.revoke_license(license_id, data)


@router.get("")
async def get_licenses(
        service: license_dep,
        status: LicenseStatus | None = None,
        key: str | None = None,
        customer_id: UUID | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        ) -> PaginationLicense:
    """ручка получения списка всех лицензий в формате пагинации с фильтрами"""
    return await service.get_licenses(
        status=status,
        key=key,
        customer_id=customer_id,
        limit=limit,
        offset=offset)
