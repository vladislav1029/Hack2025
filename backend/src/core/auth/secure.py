import jwt
from datetime import datetime, timezone, timedelta

from structlog import get_logger

from src.config import Auth
from src.core.exceptions import InvalidTokenError
from src.core.models.role import Role
from .dto import TokenAccessDict, TokenRefreshDict

log = get_logger()


class JwtHandler:
    def __init__(self, settings: Auth):
        self.settings: Auth = settings

    def create_access_token(self, oid: str, role: Role):
        sub = oid
        iat = int(datetime.now(timezone.utc).timestamp())
        exp = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.access_token_time
        )

        token = self._generate_access_token(
            TokenAccessDict(
                sub=sub,
                exp=int(exp.timestamp()),
                iat=iat,
                role=role,
            )
        )
        return token

    def create_refresh_token(self, oid: str, jti: str) -> tuple[str, datetime]:
        sub = oid
        iat = int(datetime.now(timezone.utc).timestamp())
        exp = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.refresh_token_time
        )
        token = self._generate_refresh_token(
            TokenRefreshDict(
                sub=sub,
                exp=int(exp.timestamp()),
                iat=iat,
                jti=jti,
            )
        )
        return token, exp

    def _generate_access_token(self, token: TokenAccessDict) -> str:
        return jwt.encode(
            token, key=self.settings.PRIVATE_KEY, algorithm=self.settings.algoritm
        )

    def _generate_refresh_token(self, token: TokenRefreshDict) -> str:
        return jwt.encode(
            token, key=self.settings.PRIVATE_KEY, algorithm=self.settings.algoritm
        )

    def decode_access_token(self, token: str) -> TokenAccessDict:
        try:
            payload = jwt.decode(
                token, key=self.settings.PUBLIC_KEY, algorithms=[self.settings.algoritm]
            )
            return TokenAccessDict(**payload)
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
            log.info(f"Произошла ошибка с токеном :{e}")
            raise InvalidTokenError()

    def decode_refresh_token(self, token: str) -> TokenRefreshDict:
        try:
            payload = jwt.decode(
                token, key=self.settings.PUBLIC_KEY, algorithms=[self.settings.algoritm]
            )
            return TokenRefreshDict(**payload)
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise InvalidTokenError()
