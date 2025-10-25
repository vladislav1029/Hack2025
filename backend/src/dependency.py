__all__ = [
    "DepPrivateMinioHand",
    "DepPublicMinioHand",
    "DepPasswordHasher",
    "DepUserRep",
    "DepTokenRep",
    "DepFinancialPeriodRep",
    "DepProjectHistoryRep",
    "DepProjectRep",
    "DepStageRep",
    "DepCommentRep",
    "DepServiceRep",
    "DepCostTypeRep",
    "DepCostStatusRep",
    "DepRevenueStatusRep",
    "DepPaymentTypeRep",
    "DepEvaluationTypeRep",
    "DepBusinessSegmentRep",
]
from typing import Annotated
from fastapi import Depends, Request
from minio import Minio

from src.card_of_poject.repository import (
    FinancialPeriodRepository,
    StageRepository,
    CommentRepository,
    ServiceRepository,
    CostTypeRepository,
    CostStatusRepository,
    RevenueStatusRepository,
    PaymentTypeRepository,
    EvaluationTypeRepository,
    BusinessSegmentRepository,
    ProjectHistoryRepository,
    ProjectRepository,
)
from src.config import Settings
from src.core.auth.hasher import PasswordHasher
from src.core.auth.repository import TokenRepository
from src.core.auth.secure import JwtHandler
from src.core.exceptions import ExternalServiceError
from src.core.minio.handler import MinioHandler
from structlog import get_logger
from src.core.repository import UserRepository
from src.database import AsyncSessionDep

log = get_logger()


def get_minio_private_handler(request: Request) -> MinioHandler:
    client: Minio = request.app.state.minio_client
    settings: Settings = request.app.state.settings
    if not isinstance(settings.minio.private_bucket, str):
        log.warn(f"Приватный бакет не существует {settings.minio.private_bucket}")
        raise ExternalServiceError()
    else:
        private_bucket: str = settings.minio.private_bucket
        return MinioHandler(
            client=client,
            bucket=private_bucket,
        )


def get_minio_public_handler(request: Request) -> MinioHandler:
    client: Minio = request.app.state.minio_client
    settings: Settings = request.app.state.settings
    if not isinstance(settings.minio.public_bucket, str):
        log.warn(f"Публичного бакета не существует {settings.minio.public_bucket}")
        raise ExternalServiceError()
    else:
        public_bucket: str = settings.minio.public_bucket
        return MinioHandler(
            client=client,
            bucket=public_bucket,
        )


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_handler(request: Request) -> JwtHandler:
    return JwtHandler(request.app.state.settings.auth)


DepPublicMinioHand = Annotated[MinioHandler, Depends(get_minio_public_handler)]
DepPrivateMinioHand = Annotated[MinioHandler, Depends(get_minio_private_handler)]
DepPasswordHasher = Annotated[PasswordHasher, Depends(get_password_hasher)]
DepJwtHandler = Annotated[JwtHandler, Depends(get_jwt_handler)]


async def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(session)


async def get_token_repository(session: AsyncSessionDep) -> TokenRepository:
    return TokenRepository(session)


DepUserRep = Annotated[UserRepository, Depends(get_user_repository)]
DepTokenRep = Annotated[TokenRepository, Depends(get_token_repository)]


async def get_financial_period_repository(
    session: AsyncSessionDep,
) -> FinancialPeriodRepository:
    return FinancialPeriodRepository(session)


async def get_project_history_repository(
    session: AsyncSessionDep,
) -> ProjectHistoryRepository:
    return ProjectHistoryRepository(session)


async def get_project_repository(session: AsyncSessionDep) -> ProjectRepository:
    return ProjectRepository(session)


async def get_stage_repository(session: AsyncSessionDep) -> StageRepository:
    return StageRepository(session)


async def get_comment_repository(session: AsyncSessionDep) -> CommentRepository:
    return CommentRepository(session)


async def get_service_repository(session: AsyncSessionDep) -> ServiceRepository:
    return ServiceRepository(session)


async def get_cost_type_repository(session: AsyncSessionDep) -> CostTypeRepository:
    return CostTypeRepository(session)


async def get_cost_status_repository(session: AsyncSessionDep) -> CostStatusRepository:
    return CostStatusRepository(session)


async def get_revenue_status_repository(
    session: AsyncSessionDep,
) -> RevenueStatusRepository:
    return RevenueStatusRepository(session)


async def get_payment_type_repository(
    session: AsyncSessionDep,
) -> PaymentTypeRepository:
    return PaymentTypeRepository(session)


async def get_evaluation_type_repository(
    session: AsyncSessionDep,
) -> EvaluationTypeRepository:
    return EvaluationTypeRepository(session)


async def get_business_segment_repository(
    session: AsyncSessionDep,
) -> BusinessSegmentRepository:
    return BusinessSegmentRepository(session)


# === Зависимости для DI ===

DepFinancialPeriodRep = Annotated[
    FinancialPeriodRepository, Depends(get_financial_period_repository)
]
DepProjectHistoryRep = Annotated[
    ProjectHistoryRepository, Depends(get_project_history_repository)
]
DepProjectRep = Annotated[ProjectRepository, Depends(get_project_repository)]
DepStageRep = Annotated[StageRepository, Depends(get_stage_repository)]
DepCommentRep = Annotated[CommentRepository, Depends(get_comment_repository)]
DepServiceRep = Annotated[ServiceRepository, Depends(get_service_repository)]
DepCostTypeRep = Annotated[CostTypeRepository, Depends(get_cost_type_repository)]
DepCostStatusRep = Annotated[CostStatusRepository, Depends(get_cost_status_repository)]
DepRevenueStatusRep = Annotated[
    RevenueStatusRepository, Depends(get_revenue_status_repository)
]
DepPaymentTypeRep = Annotated[
    PaymentTypeRepository, Depends(get_payment_type_repository)
]
DepEvaluationTypeRep = Annotated[
    EvaluationTypeRepository, Depends(get_evaluation_type_repository)
]
DepBusinessSegmentRep = Annotated[
    BusinessSegmentRepository, Depends(get_business_segment_repository)
]
