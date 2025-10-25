__all__ = [
    "DepPrivateMinioHand",
    "DepPublicMinioHand",
    "DepPasswordHasher",
    "DepUserRep",
    "DepTokenRep",
]
from typing import Annotated
from fastapi import Depends, Request
from minio import Minio

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
