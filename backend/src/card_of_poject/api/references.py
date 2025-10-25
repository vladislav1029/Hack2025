__all__ = ["router"]
from asyncpg import InsufficientResourcesError
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
        raise InsufficientResourcesError()
    if  await repo_stage.get_by_name(stage.name):
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
        raise InsufficientResourcesError()

    update_services = await repo_stage.update(
        stage_id, new_stage
    )
    return update_services


@router.delete("/stages/{stage_id}")
async def delete_stage(
    stage_id: PyUUID,
    user_model: DepCurrentUser,
    repo_stage: DepStageRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
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


# Пример для Service


@router.post(
    "/service",
    response_model=ServiceResponse,
)
async def create_srevice(
    service: ServiceCreate,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    service_data = Service(oid=oid, **service.model_dump())
    created_service = await repo_service.add(service_data)
    return created_service


@router.get("/service/{service_id}", response_model=ServiceResponse)
async def get_stage(service_id: PyUUID, repo_service: DepServiceRep):
    stage = await repo_service.get(service_id)
    if not stage:
        raise ResourceNotFoundError()
    return stage


@router.put(
    "/service/{service_id}",
    response_model=ServiceResponse,
)
async def update_service(
    service_id: PyUUID,
    new_service: ServiceCreate,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    service = await repo_service.get(service_id)
    if not service:
        raise ResourceNotFoundError()
    update_model = Service(
        oid=service.oid, **new_service.model_dump(exclude_unset=True)
    )
    update_services = await repo_service.add(update_model)
    return update_services


@router.delete("/service/{service_id}")
async def delete_stage(
    service_id: PyUUID,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    stage = await repo_service.get(service_id)
    if not stage:
        raise ResourceNotFoundError()
    await repo_service.delete(service_id)
    return {"message": "Stage deleted"}


@router.get("/service", response_model=List[ServiceResponse])
async def list_stages(
    repo_service: DepServiceRep,
):
    stages = await repo_service.list()
    return stages


# Добавить аналогичные CRUD для PaymentType, BusinessSegment, EvaluationType, CostType, RevenueStatus, CostStatus


# Пример для PaymentType


@router.post(
    "/payment",
    response_model=PaymentTypeResponse,
)
async def create_payment(
    payment: PaymentTypeCreate,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    service_data = PaymentType(oid=oid, **payment.model_dump())
    created_service = await repo_payment.add(service_data)
    return created_service


@router.get("/payment/{payment}", response_model=PaymentTypeResponse)
async def get_stage(payment_id: PyUUID, repo_payment: DepServiceRep):
    payment = await repo_payment.get(payment_id)
    if not payment:
        raise ResourceNotFoundError()
    return payment


@router.put(
    "/payment/{payment_id}",
    response_model=PaymentTypeResponse,
)
async def update_payment(
    payment_id: PyUUID,
    new_payment: PaymentTypeCreate,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    payment = await repo_payment.get(payment_id)
    if not payment:
        raise ResourceNotFoundError()
    update_model = PaymentType(
        oid=payment.oid, **new_payment.model_dump(exclude_unset=True)
    )
    update_payment = await repo_payment.add(update_model)
    return update_payment


@router.delete("/payment/{payment_id}")
async def delete_stage(
    payment_id: PyUUID,
    user_model: DepCurrentUser,
    repo_payment: DepPaymentTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    payment = await repo_payment.get(payment_id)
    if not payment:
        raise ResourceNotFoundError()
    await repo_payment.delete(payment_id)
    return {"message": "payment deleted"}


@router.get("/payment", response_model=List[PaymentTypeResponse])
async def list_payment(
    repo_payment: DepPaymentTypeRep,
):
    payment = await repo_payment.list()
    return payment


# Пример для BusinessSegment


@router.post(
    "/business_segment",
    response_model=BusinessSegmentResponse,
)
async def create_business_segment(
    business_segment: BusinessSegmentCreate,
    user_model: DepCurrentUser,
    repo_business_segment: DepBusinessSegmentRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    segment_data = BusinessSegment(oid=oid, **business_segment.model_dump())
    created_segment = await repo_business_segment.add(segment_data)
    return created_segment


@router.get(
    "/business_segment/{business_segment_id}", response_model=BusinessSegmentResponse
)
async def get_stage(
    business_segment_id: PyUUID, repo_business_segment: DepBusinessSegmentRep
):
    service = await repo_business_segment.get(business_segment_id)
    if not service:
        raise ResourceNotFoundError()
    return service


@router.put(
    "/business_segment/{business_segment_id}",
    response_model=PaymentTypeResponse,
)
async def update_business(
    business_segment_id: PyUUID,
    new_business_segment: BusinessSegmentCreate,
    user_model: DepCurrentUser,
    repo_business_segment: DepBusinessSegmentRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    business_segment = await repo_business_segment.get(business_segment_id)
    if not business_segment:
        raise ResourceNotFoundError()
    update_model = BusinessSegment(
        oid=business_segment.oid, **new_business_segment.model_dump(exclude_unset=True)
    )
    update_business_segment = await repo_business_segment.add(update_model)
    return update_business_segment


@router.delete("/business_segment/{business_segment_id}")
async def delete_stage(
    service_id: PyUUID,
    user_model: DepCurrentUser,
    repo_service: DepServiceRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    service = await repo_service.get(service_id)
    if not service:
        raise ResourceNotFoundError()
    await repo_service.delete(service_id)
    return {"message": "Service deleted"}


@router.get("/business_segment", response_model=List[BusinessSegmentResponse])
async def list_service(
    repo_business_segment: DepBusinessSegmentRep,
):
    service = await repo_business_segment.list()
    return service


# Пример для EvaluationType


@router.post(
    "/evaluation",
    response_model=EvaluationTypeResponse,
)
async def create_evaluation(
    evaluation: EvaluationTypeCreate,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    evaluation_data = EvaluationType(oid=oid, **evaluation.model_dump())
    created_service = await repo_evaluation.add(evaluation)
    return created_service


@router.get("/evaluation/{evaluation_id}", response_model=EvaluationTypeResponse)
async def get_stage(evaluation_id: PyUUID, repo_evaluation: DepEvaluationTypeRep):
    evaluation = await repo_evaluation.get(evaluation_id)
    if not evaluation:
        raise ResourceNotFoundError()
    return evaluation


@router.put(
    "/evaluation/{evaluation_id}",
    response_model=EvaluationTypeResponse,
)
async def update_evalution(
    evaluation_id: PyUUID,
    new_evaluation: EvaluationTypeCreate,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    evaluation = await repo_evaluation.get(evaluation_id)
    if not evaluation:
        raise ResourceNotFoundError()
    update_model = EvaluationType(
        oid=evaluation.oid, **new_evaluation.model_dump(exclude_unset=True)
    )
    update_evaluation = await repo_evaluation.add(update_model)
    return update_evaluation


@router.delete("/evaluation/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: PyUUID,
    user_model: DepCurrentUser,
    repo_evaluation: DepEvaluationTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    stage = await repo_evaluation.get(evaluation_id)
    if not stage:
        raise ResourceNotFoundError()
    await repo_evaluation.delete(evaluation_id)
    return {"message": "Evaluation deleted"}


@router.get("/evaluations", response_model=List[EvaluationTypeResponse])
async def list_evaluation(
    repo_evaluation: DepEvaluationTypeRep,
):
    evaluation = await repo_evaluation.list()
    return evaluation


# Пример для CostType


@router.post(
    "/cost",
    response_model=CostTypeResponse,
)
async def create_cost(
    cost: CostTypeCreate,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    cost_data = CostType(oid=oid, **cost.model_dump())
    created_cost = await repo_cost.add(cost_data)
    return created_cost


@router.get("/cost/{cost_id}", response_model=CostTypeResponse)
async def get_cost(cost_id: PyUUID, repo_cost: DepCostTypeRep):
    cost = await repo_cost.get(cost_id)
    if not cost:
        raise ResourceNotFoundError()
    return cost


@router.put(
    "/cost/{cost_id}",
    response_model=CostTypeResponse,
)
async def update_evalution(
    cost_id: PyUUID,
    new_cost: CostTypeCreate,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    cost = await repo_cost.get(cost_id)
    if not cost:
        raise ResourceNotFoundError()
    update_model = CostType(oid=cost.oid, **new_cost.model_dump(exclude_unset=True))
    update_cost = await repo_cost.add(update_model)
    return update_cost


@router.delete("/cost/{cost_id}")
async def delete_cost(
    cost_id: PyUUID,
    user_model: DepCurrentUser,
    repo_cost: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    cost = await repo_cost.get(cost_id)
    if not cost:
        raise ResourceNotFoundError()
    await repo_cost.delete(cost_id)
    return {"message": "cost deleted"}


@router.get("/cost", response_model=List[CostTypeResponse])
async def list_CostResponce(
    repo_cost: DepCostTypeRep,
):
    cost = await repo_cost.list()
    return cost


# Пример для RevenueStatus


@router.post(
    "/revenue_status",
    response_model=RevenueStatusResponse,
)
async def create_revenue_status(
    revenue_status: RevenueStatusCreate,
    user_model: DepCurrentUser,
    repo_revenue_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    service_data = RevenueStatus(oid=oid, **revenue_status.model_dump())
    created_revenue_status = await repo_revenue_status.add(service_data)
    return created_revenue_status


@router.get("/revenue_status/{revenue_status_id}", response_model=RevenueStatusResponse)
async def get_revenue_status(
    revenue_status_id: PyUUID, repo_revenue_status: DepRevenueStatusRep
):
    revenue_status = await repo_revenue_status.get(revenue_status_id)
    if not revenue_status:
        raise ResourceNotFoundError()
    return revenue_status


@router.put(
    "/revenue_status/{revenue_status_id}",
    response_model=RevenueStatusResponse,
)
async def update_evalution(
    revenue_status_id: PyUUID,
    new_revenue_status: RevenueStatusCreate,
    user_model: DepCurrentUser,
    repo_revenue_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    revenue_status = await repo_revenue_status.get(revenue_status_id)
    if not revenue_status:
        raise ResourceNotFoundError()
    update_model = RevenueStatus(
        oid=revenue_status.oid, **new_revenue_status.model_dump(exclude_unset=True)
    )
    update_revenue_status = await repo_revenue_status.add(update_model)
    return update_revenue_status


@router.delete("/revenue_status/{revenue_status_id}")
async def delete_revenue_status(
    revenue_status_id: PyUUID,
    user_model: DepCurrentUser,
    repo_revenue_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    revenue_status = await repo_revenue_status.get(revenue_status_id)
    if not revenue_status:
        raise ResourceNotFoundError()
    await repo_revenue_status.delete(revenue_status_id)
    return {"message": "revenue_status deleted"}


@router.get("/revenue_statuses", response_model=List[RevenueStatusResponse])
async def list_revenue_status(
    repo_revenue_status: DepRevenueStatusRep,
):
    revenue_status = await repo_revenue_status.list()
    return revenue_status


# Пример для CostStatus


@router.post(
    "/cost_status",
    response_model=CostStatusResponse,
)
async def create_cost_status(
    cost_status: ServiceCreate,
    user_model: DepCurrentUser,
    repo_cost_status: DepCostStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    oid = uuid4()
    service_data = CostStatus(oid=oid, **cost_status.model_dump())
    created_cost_status = await repo_cost_status.add(service_data)
    return created_cost_status


@router.get("/cost_status/{cost_status_id}", response_model=CostStatusResponse)
async def get_cost_status(cost_status_id: PyUUID, repo_cost_status: DepCostStatusRep):
    cost_status = await repo_cost_status.get(cost_status_id)
    if not cost_status:
        raise ResourceNotFoundError()
    return cost_status


@router.put(
    "/cost_status/{cost_status_id}",
    response_model=CostStatusResponse,
)
async def update_evalution(
    cost_status_id: PyUUID,
    new_cost_status: RevenueStatusCreate,
    user_model: DepCurrentUser,
    repo_cost_status: DepRevenueStatusRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    cost_status = await repo_cost_status.get(cost_status_id)
    if not cost_status:
        raise CostStatus()
    update_model = RevenueStatus(
        oid=cost_status.oid, **new_cost_status.model_dump(exclude_unset=True)
    )
    update_cost_status = await repo_cost_status.add(update_model)
    return update_cost_status


@router.delete("/cost_status/{cost_status_id}")
async def delete_cost_status(
    cost_status_id: PyUUID,
    user_model: DepCurrentUser,
    repo_cost_status: DepCostTypeRep,
):
    user_id, user_role = user_model
    if user_role != Role.ADMIN:
        raise InsufficientResourcesError()
    stage = await repo_cost_status.get(cost_status_id)
    if not stage:
        raise ResourceNotFoundError()
    await repo_cost_status.delete(cost_status_id)
    return {"message": "cost_status deleted"}


@router.get("/cost_status", response_model=List[CostStatusResponse])
async def list_cost_status(
    repo_cost_status: DepCostTypeRep,
):
    stages = await repo_cost_status.list()
    return stages
