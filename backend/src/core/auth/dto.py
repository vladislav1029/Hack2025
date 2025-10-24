from typing import TypedDict

from src.core.models.role import Role


class TokenAccessDict(TypedDict):
    sub: str
    exp: int
    iat: int
    role: Role


class TokenRefreshDict(TypedDict):
    sub: str
    exp: int
    iat: int
    jti: str
