from re import L
from typing import Annotated
import uuid
from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from src.core.auth.dto import TokenAccessDict
from src.core.exceptions import InvalidTokenError as CustomInvalidTokenError
from src.dependensy import DepJwtHandler
from structlog import get_logger

log = get_logger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")


async def get_current_user(
    jwt_handler: DepJwtHandler,
    token: str = Depends(oauth2_scheme),
) -> tuple[UUID, int]:
    log.debug("Начало проверки токена")
    try:
        payload: TokenAccessDict = jwt_handler.decode_access_token(token)
        user_id_str, role = payload["sub"], payload["role"]
        if not user_id_str or role is None:
            log.debug("Токен без user_id, или role")
            raise CustomInvalidTokenError()

        user_id = uuid.UUID(user_id_str)
        log.debug("Токен удачно прошёл проверки")
        return user_id, role
    except (InvalidTokenError, ValueError) as e:
        log.debug(f"Ошибка по причине : {e}")
        raise CustomInvalidTokenError()


DepCurrentUser = Annotated[tuple[UUID, int], Depends(get_current_user)]
