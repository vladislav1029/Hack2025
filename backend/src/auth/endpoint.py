from typing import Annotated
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Cookie, Depends, Request, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import jwt
from structlog import get_logger

from src.auth.schemas import TokenResponse, UserRegister, UserResponse
from src.auth.schemas import (
    AuthResponse,
)
from src.core.auth.current import DepCurrentUser
from src.core.auth.dto import TokenRefreshDict
from src.core.models.role import Role
from src.dependency import DepJwtHandler, DepPasswordHasher, DepTokenRep, DepUserRep
from src.core.auth.models import User
from src.core.exceptions import (
    InvalidInputError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
    UnauthorizedError,
    UserNotFoundError,
)
from src.core.exceptions import InvalidTokenError as CustomInvalidTokenError

router = APIRouter(tags=["auth"])

log = get_logger()


# WARN: uuid.UUID() плохая конструкция из-за неадаптивности кода должно быть что-то IDValue.
# WARN: По нормальномы вынести либо в use case, либо в iterator
@router.post(
    "/",
    response_model=AuthResponse,
    description="Регистрация пользователя.",
)
async def registery(
    user: UserRegister,
    user_repo: DepUserRep,
    jwt_handler: DepJwtHandler,
    token_repo: DepTokenRep,
    hasher: DepPasswordHasher,
    response: Response,
) -> AuthResponse:
    user_in_db = await user_repo.get_by_email(user.email)
    if user_in_db:
        raise ResourceAlreadyExistsError()
    log.debug(f"Пароль пользователя: {user.password}")
    password = hasher.hash_password(user.password)
    user_id = uuid.uuid4()
    model = User(
        oid=user_id,
        email=user.email,
        password=password,
        created_at=datetime.now(timezone.utc),
        update_at=None,
    )
    refresh_token_jti = uuid.uuid4()

    resp = await user_repo.add(model)
    refresh_token, expired_at = jwt_handler.create_refresh_token(
        str(user_id), str(refresh_token_jti)
    )
    access_token = jwt_handler.create_access_token(str(user_id), role=Role.USER)

    await token_repo.create(
        user_id=user_id, jti=refresh_token_jti, expired_at=expired_at
    )
    # Устанавливаем cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=jwt_handler.settings.refresh_token_time,
        samesite="lax",
        secure=False,  # WARN: стоит исправить secure при продакшене
    )

    return AuthResponse(
        user=UserResponse.model_validate(resp),
        access_token=access_token,
    )


@router.get("/me", response_model=UserResponse)
async def user_for_oid(repo: DepUserRep, user_data: DepCurrentUser) -> UserResponse:
    user_id, user_role = user_data

    result = await repo.get(user_id)
    if not result:
        raise ResourceNotFoundError()
    return UserResponse.model_validate(result)


@router.post("/login", description="User login", response_model=AuthResponse)
async def login_user(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: DepUserRep,
    jwt_handler: DepJwtHandler,
    token_repo: DepTokenRep,
    hasher: DepPasswordHasher,
    response: Response,
) -> AuthResponse:
    user = await user_repo.get_by_email(form.username)
    if not user:
        raise UserNotFoundError()

    if not hasher.verify_password(form.password, user.password):
        raise InvalidInputError()

    refresh_token_jti = uuid.uuid4()

    refresh_token, expired_at = jwt_handler.create_refresh_token(
        str(user.oid), str(refresh_token_jti)
    )
    access_token = jwt_handler.create_access_token(str(user.oid), user.role)

    await token_repo.create(
        user_id=user.oid, jti=refresh_token_jti, expired_at=expired_at
    )
    # Устанавливаем cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=jwt_handler.settings.refresh_token_time,
        samesite="lax",
        secure=False,  # WARN: стоит исправить secure при продакшене
    )

    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
    )


@router.get(
    "/refresh",
    description="Обновление токенов при просроченности access token",
)
async def refresh_token(
    request: Request,
    response: Response,
    jwt_handler: DepJwtHandler,
    token_repo: DepTokenRep,
    user_repo: DepUserRep,
) -> TokenResponse:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        log.info("No refresh token provided")
        raise UnauthorizedError()
    try:
        token_data = jwt_handler.decode_refresh_token(refresh_token)
        jti = uuid.UUID(token_data["jti"])
        user_id = uuid.UUID(token_data["sub"])
        if not await token_repo.is_valid(jti):
            raise UnauthorizedError()
        user = await user_repo.get(user_id)
        if not user:
            raise UserNotFoundError()
        await token_repo.delete(jti)
        new_jti = str(uuid.uuid4())
        new_refresh_token, expired_at = jwt_handler.create_refresh_token(
            str(user_id),
            new_jti,
        )
        await token_repo.create(
            user_id=user_id,
            jti=new_jti,
            expired_at=expired_at,
        )
        new_access_token = jwt_handler.create_access_token(
            str(user_id),
            role=user.role,
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            max_age=jwt_handler.settings.refresh_token_time,
            samesite="lax",
            secure=False,
        )
        return TokenResponse(access_token=new_access_token)
    except (jwt.InvalidTokenError, ValueError):
        raise UnauthorizedError()


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    jwt_handler: DepJwtHandler,
    token_repo: DepTokenRep,
) -> dict:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedError()

    try:
        # Декодируем refresh_token, чтобы получить jti
        token_data: TokenRefreshDict = jwt_handler.decode_refresh_token(refresh_token)

        jti = token_data["jti"]

        # Инвалидируем refresh_token в TokenRepo
        await token_repo.delete(uuid.UUID(jti))

        # Удаляем cookie
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            samesite="lax",
            secure=False,  # WARN: стоит исправить secure при продакшене
        )

        return {"message": "Logged out"}
    except jwt.InvalidTokenError:
        raise CustomInvalidTokenError()
