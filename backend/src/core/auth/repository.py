from datetime import datetime, timezone
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from src.core.auth.models import RefreshToken
from src.core.repository import IDType


log = get_logger()


class TokenRepository:  # INFO: не наследуемся от AbstractRepository не сходимся по методам
    model = RefreshToken

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, oid: IDType):
        return await self.session.get(self.model, oid)

    async def create(
        self, user_id: IDType, jti: IDType, expired_at: datetime
    ) -> RefreshToken:
        created_at = datetime.now(timezone.utc)
        token = self.model(
            oid=jti,
            user_id=user_id,
            expired_at=expired_at,
            created_at=created_at,
        )
        self.session.add(token)
        await self.session.commit()
        return token

    async def delete(self, jti: IDType) -> None:
        jti_uuid = jti  #
        await self.session.execute(
            delete(self.model).where(self.model.oid == jti_uuid)
        )
        await self.session.commit()

    async def is_valid(self, jti: IDType) -> bool:
        jti_uuid = jti
        result = await self.session.execute(
            select(self.model).where(
                self.model.oid == jti_uuid,
                self.model.expired_at > datetime.now(timezone.utc)
            )
        )
        return result.scalar_one_or_none() is not None