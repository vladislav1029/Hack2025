__all__ = ["router"]
from fastapi import APIRouter


from uuid import UUID as PyUUID, uuid4
from typing import List

from src.card_of_poject.model import (
    BusinessSegment,
    CostStatus,
    CostType,
    EvaluationType,
    PaymentType,
    RevenueStatus,
    Service,
    Stage,
)

from src.card_of_poject.repository.references import ServiceRepository
from src.card_of_poject.schemas.references import (
    BusinessSegmentCreate,
    BusinessSegmentResponse,
    CostStatusCreate,
    CostStatusResponse,
    CostTypeCreate,
    CostTypeResponse,
    EvaluationTypeCreate,
    EvaluationTypeResponse,
    PaymentTypeCreate,
    PaymentTypeResponse,
    RevenueStatusCreate,
    RevenueStatusResponse,
    ServiceCreate,
    ServiceResponse,
    StageCreate,
    StageResponse,
)
from src.core.auth.current import DepCurrentUser
from src.core.auth.models import User
from src.core.exceptions import (
    InsufficientPermissionsError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
    UserNotFoundError,
)

from src.core.models.role import Role
from src.dependency import (
    DepBusinessSegmentRep,
    DepCostStatusRep,
    DepCostTypeRep,
    DepEvaluationTypeRep,
    DepPaymentTypeRep,
    DepRevenueStatusRep,
    DepServiceRep,
    DepStageRep,
)
from structlog import get_logger

router = APIRouter(prefix="/references", tags=["References"])

log = get_logger(__name__)


@router.post(
    "/stages",
    response_model=StageResponse,
)
async def create_stage(
    stage: StageCreate,
    user_model: DepCurrentUser,
    repo_stage: DepStageRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_stage.get_by_name(stage.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    log.debug(f"Creating stage {stage.model_dump()},\n")
    stage_data = Stage(oid=oid, **stage.model_dump())
    created_stage = await repo_stage.add(stage_data)
    return created_stage


@router.get("/stages/{stage_id}", response_model=StageResponse)
async def get_stage(stage_id: PyUUID, repo_stage: DepStageRep):
    stage = await repo_stage.get(stage_id)
    if not stage:
        raise ResourceNotFoundError()
    return stage


@router.put(
    "/stages/{stage_id}",
    response_model=StageResponse,
)
async def update_stage(
    stage_id: PyUUID,
    new_stage: StageCreate,
    user_model: DepCurrentUser,
    repo_stage: DepStageRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()

    update_services = await repo_stage.update(stage_id, new_stage)
    return update_services


@router.delete("/stages/{stage_id}")
async def delete_services(
    stage_id: PyUUID,
    user_model: DepCurrentUser,
    repo_stage: DepStageRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    stage = await repo_stage.get(stage_id)
    if not stage:
        raise ResourceNotFoundError()
    await repo_stage.delete(stage_id)
    return {"message": "Stage deleted"}


@router.get("/stages", response_model=List[StageResponse])
async def list_stages(
    repo_stage: DepStageRep,
):
    stages = await repo_stage.list()
    return stages


# === SERVICES ===
@router.post("/service", response_model=ServiceResponse)
async def create_service(
    service: ServiceCreate,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()

    if await repo_service.get_by_name(service.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    service_data = Service(oid=oid, **service.model_dump())
    return await repo_service.add(service_data)


@router.get("/service/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: PyUUID, repo_service: DepServiceRep):
    service = await repo_service.get(service_id)
    if not service:
        raise ResourceNotFoundError()
    return service


@router.put("/service/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: PyUUID,
    new_service: ServiceCreate,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_service.get(service_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_service.name != existing.name and await repo_service.get_by_name(
        new_service.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_service.update(
        service_id, new_service.model_dump(exclude_unset=True)
    )


@router.delete("/service/{service_id}")
async def delete_service(
    service_id: PyUUID,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    service = await repo_service.get(service_id)
    if not service:
        raise ResourceNotFoundError()
    await repo_service.delete(service_id)
    return {"message": "Service deleted"}


@router.get("/service", response_model=List[ServiceResponse])
async def list_services(repo_service: DepServiceRep):
    return await repo_service.list()


# Добавить аналогичные CRUD для PaymentType, BusinessSegment, EvaluationType, CostType, RevenueStatus, CostStatus


# === PAYMENT TYPES ===
@router.post("/payment", response_model=PaymentTypeResponse)
async def create_payment_type(
    payment: PaymentTypeCreate,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_payment.get_by_name(payment.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    payment_data = PaymentType(oid=oid, **payment.model_dump())
    return await repo_payment.add(payment_data)


@router.get("/payment/{payment_id}", response_model=PaymentTypeResponse)
async def get_payment_type(payment_id: PyUUID, repo_payment: DepPaymentTypeRep):
    payment = await repo_payment.get(payment_id)
    if not payment:
        raise ResourceNotFoundError()
    return payment


@router.put("/payment/{payment_id}", response_model=PaymentTypeResponse)
async def update_payment_type(
    payment_id: PyUUID,
    new_payment: PaymentTypeCreate,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_payment.get(payment_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_payment.name != existing.name and await repo_payment.get_by_name(
        new_payment.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_payment.update(
        payment_id, new_payment.model_dump(exclude_unset=True)
    )


@router.delete("/payment/{payment_id}")
async def delete_payment_type(
    payment_id: PyUUID,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    payment = await repo_payment.get(payment_id)
    if not payment:
        raise ResourceNotFoundError()
    await repo_payment.delete(payment_id)
    return {"message": "Payment type deleted"}


@router.get("/payment", response_model=List[PaymentTypeResponse])
async def list_payment_types(repo_payment: DepPaymentTypeRep):
    return await repo_payment.list()


# === BUSINESS SEGMENTS ===
@router.post("/business_segment", response_model=BusinessSegmentResponse)
async def create_business_segment(
    segment: BusinessSegmentCreate,
    user_model: DepCurrentUser,
    repo_segment: DepBusinessSegmentRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_segment.get_by_name(segment.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    segment_data = BusinessSegment(oid=oid, **segment.model_dump())
    return await repo_segment.add(segment_data)


@router.get("/business_segment/{segment_id}", response_model=BusinessSegmentResponse)
async def get_business_segment(segment_id: PyUUID, repo_segment: DepBusinessSegmentRep):
    segment = await repo_segment.get(segment_id)
    if not segment:
        raise ResourceNotFoundError()
    return segment


@router.put("/business_segment/{segment_id}", response_model=BusinessSegmentResponse)
async def update_business_segment(
    segment_id: PyUUID,
    new_segment: BusinessSegmentCreate,
    user_model: DepCurrentUser,
    repo_segment: DepBusinessSegmentRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_segment.get(segment_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_segment.name != existing.name and await repo_segment.get_by_name(
        new_segment.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_segment.update(
        segment_id, new_segment.model_dump(exclude_unset=True)
    )


@router.delete("/business_segment/{segment_id}")
async def delete_business_segment(
    segment_id: PyUUID,
    user_model: DepCurrentUser,
    repo_segment: DepBusinessSegmentRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    segment = await repo_segment.get(segment_id)
    if not segment:
        raise ResourceNotFoundError()
    await repo_segment.delete(segment_id)
    return {"message": "Business segment deleted"}


@router.get("/business_segment", response_model=List[BusinessSegmentResponse])
async def list_business_segments(repo_segment: DepBusinessSegmentRep):
    return await repo_segment.list()


# === EVALUATION TYPES ===
@router.post("/evaluation", response_model=EvaluationTypeResponse)
async def create_evaluation_type(
    evaluation: EvaluationTypeCreate,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_evaluation.get_by_name(evaluation.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    evaluation_data = EvaluationType(oid=oid, **evaluation.model_dump())
    return await repo_evaluation.add(evaluation_data)


@router.get("/evaluation/{evaluation_id}", response_model=EvaluationTypeResponse)
async def get_evaluation_type(
    evaluation_id: PyUUID, repo_evaluation: DepEvaluationTypeRep
):
    evaluation = await repo_evaluation.get(evaluation_id)
    if not evaluation:
        raise ResourceNotFoundError()
    return evaluation


@router.put("/evaluation/{evaluation_id}", response_model=EvaluationTypeResponse)
async def update_evaluation_type(
    evaluation_id: PyUUID,
    new_evaluation: EvaluationTypeCreate,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_evaluation.get(evaluation_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_evaluation.name != existing.name and await repo_evaluation.get_by_name(
        new_evaluation.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_evaluation.update(
        evaluation_id, new_evaluation.model_dump(exclude_unset=True)
    )


@router.delete("/evaluation/{evaluation_id}")
async def delete_evaluation_type(
    evaluation_id: PyUUID,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    evaluation = await repo_evaluation.get(evaluation_id)
    if not evaluation:
        raise ResourceNotFoundError()
    await repo_evaluation.delete(evaluation_id)
    return {"message": "Evaluation type deleted"}


@router.get("/evaluation", response_model=List[EvaluationTypeResponse])
async def list_evaluation_types(repo_evaluation: DepEvaluationTypeRep):
    return await repo_evaluation.list()


# Пример для CostType


# === COST TYPES ===
@router.post("/cost", response_model=CostTypeResponse)
async def create_cost_type(
    cost: CostTypeCreate,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_cost.get_by_name(cost.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    cost_data = CostType(oid=oid, **cost.model_dump())
    return await repo_cost.add(cost_data)


@router.get("/cost/{cost_id}", response_model=CostTypeResponse)
async def get_cost_type(cost_id: PyUUID, repo_cost: DepCostTypeRep):
    cost = await repo_cost.get(cost_id)
    if not cost:
        raise ResourceNotFoundError()
    return cost


@router.put("/cost/{cost_id}", response_model=CostTypeResponse)
async def update_cost_type(
    cost_id: PyUUID,
    new_cost: CostTypeCreate,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_cost.get(cost_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_cost.name != existing.name and await repo_cost.get_by_name(new_cost.name):
        raise ResourceAlreadyExistsError()
    return await repo_cost.update(cost_id, new_cost.model_dump(exclude_unset=True))


@router.delete("/cost/{cost_id}")
async def delete_cost_type(
    cost_id: PyUUID,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    cost = await repo_cost.get(cost_id)
    if not cost:
        raise ResourceNotFoundError()
    await repo_cost.delete(cost_id)
    return {"message": "Cost type deleted"}


@router.get("/cost", response_model=List[CostTypeResponse])
async def list_cost_types(repo_cost: DepCostTypeRep):
    return await repo_cost.list()


# === REVENUE STATUSES ===
@router.post("/revenue_status", response_model=RevenueStatusResponse)
async def create_revenue_status(
    status: RevenueStatusCreate,
    user_model: DepCurrentUser,
    repo_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_status.get_by_name(status.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    status_data = RevenueStatus(oid=oid, **status.model_dump())
    return await repo_status.add(status_data)


@router.get("/revenue_status/{status_id}", response_model=RevenueStatusResponse)
async def get_revenue_status(status_id: PyUUID, repo_status: DepRevenueStatusRep):
    status = await repo_status.get(status_id)
    if not status:
        raise ResourceNotFoundError()
    return status


@router.put("/revenue_status/{status_id}", response_model=RevenueStatusResponse)
async def update_revenue_status(
    status_id: PyUUID,
    new_status: RevenueStatusCreate,
    user_model: DepCurrentUser,
    repo_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_status.get(status_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_status.name != existing.name and await repo_status.get_by_name(
        new_status.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_status.update(
        status_id, new_status.model_dump(exclude_unset=True)
    )


@router.delete("/revenue_status/{status_id}")
async def delete_revenue_status(
    status_id: PyUUID,
    user_model: DepCurrentUser,
    repo_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    status = await repo_status.get(status_id)
    if not status:
        raise ResourceNotFoundError()
    await repo_status.delete(status_id)
    return {"message": "Revenue status deleted"}


@router.get("/revenue_status", response_model=List[RevenueStatusResponse])
async def list_revenue_statuses(repo_status: DepRevenueStatusRep):
    return await repo_status.list()


# Пример для CostStatus


# === COST STATUSES ===
@router.post("/cost_status", response_model=CostStatusResponse)
async def create_cost_status(
    status: CostStatusCreate,
    user_model: DepCurrentUser,
    repo_status: DepCostStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    if await repo_status.get_by_name(status.name):
        raise ResourceAlreadyExistsError()
    oid = uuid4()
    status_data = CostStatus(oid=oid, **status.model_dump())
    return await repo_status.add(status_data)


@router.get("/cost_status/{status_id}", response_model=CostStatusResponse)
async def get_cost_status(status_id: PyUUID, repo_status: DepCostStatusRep):
    status = await repo_status.get(status_id)
    if not status:
        raise ResourceNotFoundError()
    return status


@router.put("/cost_status/{status_id}", response_model=CostStatusResponse)
async def update_cost_status(
    status_id: PyUUID,
    new_status: CostStatusCreate,
    user_model: DepCurrentUser,
    repo_status: DepCostStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    existing = await repo_status.get(status_id)
    if not existing:
        raise ResourceNotFoundError()
    if new_status.name != existing.name and await repo_status.get_by_name(
        new_status.name
    ):
        raise ResourceAlreadyExistsError()
    return await repo_status.update(
        status_id, new_status.model_dump(exclude_unset=True)
    )


@router.delete("/cost_status/{status_id}")
async def delete_cost_status(
    status_id: PyUUID,
    user_model: DepCurrentUser,
    repo_status: DepCostStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    status = await repo_status.get(status_id)
    if not status:
        raise ResourceNotFoundError()
    await repo_status.delete(status_id)
    return {"message": "Cost status deleted"}


@router.get("/cost_status", response_model=List[CostStatusResponse])
async def list_cost_statuses(repo_status: DepCostStatusRep):
    return await repo_status.list()
