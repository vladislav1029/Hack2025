from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_session, require_role
from core.models.role import Role
from uuid import UUID as PyUUID
from typing import List

from src.card_of_poject.model import PaymentType, Service, Stage
from src.card_of_poject.repository.references import (
    PaymentTypeRepository,
    ServiceRepository,
    StageRepository,
)
from src.card_of_poject.schemas.references import (
    PaymentTypeResponse,
    ServiceCreate,
    ServiceResponse,
    StageCreate,
    StageResponse,
)
from src.core.auth.current import DepCurrentUser
from src.core.auth.models import User
from src.core.exceptions import InsufficientPermissionsError
from src.core.repository import UserRepository

router = APIRouter(prefix="/references", tags=["References"])


@router.post(
    "/stages",
    response_model=StageResponse,
)
async def create_stage(
    stage: StageCreate,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = UserRepository(**user_model.model_dump())
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError()
    repo = StageRepository(session, Stage)
    stage_data = Stage(**stage.model_dump(()))
    created_stage = await repo.add(stage_data)
    return created_stage


@router.get("/stages/{stage_id}", response_model=StageResponse)
async def get_stage(stage_id: PyUUID, session: AsyncSession = Depends(get_session)):
    repo = StageRepository(session, Stage)
    stage = await repo.get(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


@router.put(
    "/stages/{stage_id}",
    response_model=StageResponse,
)
async def update_stage(
    stage_id: PyUUID,
    stage: StageCreate,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = UserRepository(**user_model.model_dump())
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError()
    repo = StageRepository(session, Stage)
    existing_stage = await repo.get(stage_id)
    if not existing_stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    update_data = stage.model_dump()(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_stage, key, value)
    updated_stage = await repo.add(existing_stage)
    return updated_stage


@router.delete("/stages/{stage_id}")
async def delete_stage(
    stage_id: PyUUID,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError()
    repo = StageRepository(session, Stage)
    stage = await repo.get(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    await repo.delete(stage_id)
    return {"message": "Stage deleted"}


@router.get("/stages", response_model=List[StageResponse])
async def list_stages(session: AsyncSession = Depends(get_session)):
    repo = StageRepository(session, Stage)
    stages = await repo.list()
    return stages


# Пример для Service


@router.post(
    "/services",
    response_model=ServiceResponse,
)
async def create_service(
    service: ServiceCreate,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = UserRepository(**user_model.model_dump())
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError()
    repo = ServiceRepository(session, Service)
    service_data = Service(**service.model_dump())
    created_service = await repo.add(service_data)
    return created_service


@router.get("/services/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: PyUUID, session: AsyncSession = Depends(get_session)):
    repo = ServiceRepository(session, Service)
    service = await repo.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.put(
    "/services/{service_id}",
    response_model=ServiceResponse,
)
async def update_service(
    service_id: PyUUID,
    service: ServiceCreate,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = User(**user_model.model_dump())
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError
    repo = ServiceRepository(session, Service)
    existing_service = await repo.get(service_id)
    if not existing_service:
        raise HTTPException(status_code=404, detail="Service not found")
    update_data = service.model_dump()(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_service, key, value)
    updated_service = await repo.add(existing_service)
    return updated_service


@router.delete()
async def delete_service(
    service_id: PyUUID,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = User(**user_model.model_dump())
    if user.id != Role.ADMMIN:
        raise InsufficientPermissionsError
    repo = ServiceRepository(session, Service)
    service = await repo.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    await repo.delete(service_id)
    return {"message": "Service deleted"}


@router.get("/services", response_model=List[ServiceResponse])
async def list_services(session: AsyncSession = Depends(get_session)):
    repo = ServiceRepository(session, Service)
    services = await repo.list()
    return services


# Добавить аналогичные CRUD для PaymentType, BusinessSegment, EvaluationType, CostType, RevenueStatus, CostStatus


# Пример для PaymentType


@router.get("/payment_type/{payment_id}", responce_model=PaymentTypeResponse)
async def get_payment_type_by_id(
    payment_type: PaymentTypeRepository, session: AsyncSession = Depends(get_session)
):
    repo = PaymentTypeRepository(session, PaymentType)
    payment = await repo.get(payment_type)
    if not payment:
        raise HTTPException(status_code=404, detail="Service not found")
    return payment


@router.put(
    "/payment_type/{payment_id}",
    response_model=PaymentTypeResponse,
    responce_model=PaymentTypeResponse,
)
async def update_payment(
    payment_id: PyUUID,
    paymnet: ServiceCreate,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = User(**user_model.model_dump())
    if user.id != Role.ADMIN:
        raise InsufficientPermissionsError
    repo = PaymentTypeResponse(session, PaymentType)
    existing_service = await repo.get(payment_id)
    if not existing_service:
        raise HTTPException(status_code=404, detail="Service not found")
    update_data = paymnet.model_dump()(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_service, key, value)
    updated_service = await repo.add(existing_service)
    return updated_service


@router.delete()
async def delete_service(
    service_id: PyUUID,
    user_model: DepCurrentUser,
    session: AsyncSession = Depends(get_session),
):
    user = User(**user_model.model_dump())
    if user.id != Role.ADMMIN:
        raise InsufficientPermissionsError
    repo = ServiceRepository(session, Service)
    service = await repo.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    await repo.delete(service_id)
    return {"message": "Service deleted"}


@router.get("/services", response_model=List[ServiceResponse])
async def list_services(session: AsyncSession = Depends(get_session)):
    repo = ServiceRepository(session, Service)
    services = await repo.list()
    return services


# Пример для BusinessSegment
# Пример для EvaluationType
# Пример для CostType
# Пример для CostTRevenueStatus
# Пример для CostStatus
