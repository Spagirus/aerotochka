"""ендпоинты лицензии"""
from uuid import UUID

from fastapi import APIRouter

from src.api.dependens import license_dep
from src.application.schemas.license import CreateLicense, ReadLicense, RevokeBody

router = APIRouter(
    tags=["Licenses"],
    prefix="/api/v1/licenses"
)


@router.get("/{id}")
async def get_license(license_id: UUID, service: license_dep) -> ReadLicense:
    return await service.get_license(license_id=license_id)


@router.post("/", status_code=201)
async def add_license(data: CreateLicense, service: license_dep) -> ReadLicense:
    return await service.create_license(data)

@router.post("/{id}/suspend", status_code=200)
async def suspend_license(license_id: UUID, service: license_dep) -> ReadLicense:
    return await service.suspend_license(license_id)

@router.post("/{id}/resume", status_code=200)
async def resume_license(license_id: UUID, service: license_dep) -> ReadLicense:
    return await service.resume_license(license_id)

@router.post("/{id}/revoke", status_code=200)
async def revoke_license(license_id: UUID, service: license_dep, data:RevokeBody) -> ReadLicense:
    return await service.revoke_license(license_id, data)
