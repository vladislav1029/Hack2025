# handlers/exception_handlers.py
__all__ = ["include_all_exceptions_handlers"]
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import structlog

from .exceptions import (
    ApplicationError,
    InvalidCredentialsError,
    TokenExpiredError,
    InvalidTokenError,
    UnauthorizedError,
    InsufficientPermissionsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidInputError,
    InvalidEmailError,
    PasswordTooWeakError,
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
    ResourceConflictError,
    InsufficientFundsError,
    ActionNotAllowedError,
    RateLimitExceededError,
    FileTooLargeError,
    UnsupportedFileTypeError,
    ExternalServiceError,
)

logger = structlog.get_logger()

# Маппинг: тип ошибки → HTTP статус
_ERROR_STATUS_MAP = {
    # 400 Bad Request
    InvalidInputError: status.HTTP_400_BAD_REQUEST,
    InvalidEmailError: status.HTTP_400_BAD_REQUEST,
    PasswordTooWeakError: status.HTTP_400_BAD_REQUEST,
    FileTooLargeError: status.HTTP_400_BAD_REQUEST,
    UnsupportedFileTypeError: status.HTTP_400_BAD_REQUEST,
    ActionNotAllowedError: status.HTTP_400_BAD_REQUEST,
    ExternalServiceError: status.HTTP_400_BAD_REQUEST,
    # 401 Unauthorized
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
    UnauthorizedError: status.HTTP_401_UNAUTHORIZED,
    # 403 Forbidden
    InsufficientPermissionsError: status.HTTP_403_FORBIDDEN,
    # 404 Not Found
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    ResourceNotFoundError: status.HTTP_404_NOT_FOUND,
    # 409 Conflict
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    ResourceAlreadyExistsError: status.HTTP_409_CONFLICT,
    ResourceConflictError: status.HTTP_409_CONFLICT,
    InsufficientFundsError: status.HTTP_409_CONFLICT,
    # 429 Too Many Requests
    RateLimitExceededError: status.HTTP_429_TOO_MANY_REQUESTS,
}


async def _application_error_handler(request: Request, exc: ApplicationError):
    """Общий обработчик для всех ApplicationError и его подклассов."""
    status_code = status.HTTP_400_BAD_REQUEST
    for error_type, code in _ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            status_code = code
            break

    # Синхронное логирование — без await!
    logger.warning(
        "application_error",
        error_type=exc.__class__.__name__,
        message=exc.message,
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    return JSONResponse(status_code=status_code, content={"detail": exc.message})


def include_all_exceptions_handlers(app: FastAPI) -> FastAPI:
    """Подключает обработчик для всех кастомных ошибок приложения."""
    app.add_exception_handler(ApplicationError, _application_error_handler)
    return app
