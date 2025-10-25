from datetime import datetime, timezone
import uuid

from sqlalchemy import select
from src.core.models.role import Role
from src.database import session_maker
from src.dependency import get_password_hasher
from src.core.auth.models import User
from src.config import settings

import structlog

log = structlog.get_logger()


async def command():

    hasher = get_password_hasher()

    async with session_maker() as session:
        stmt = select(User).where(User.email == settings.admin.mail)
        result = await session.execute(stmt)
        admin = result.scalar_one_or_none()

        if admin is None:
            # Создаём только если нет
            oid = uuid.uuid4()
            hashed_password = hasher.hash_password(settings.admin.password)
            admin_user = User(
                oid=oid,
                email=settings.admin.mail,
                password=hashed_password,
                role=Role.ADMIN,
                is_active=True,
                is_verificate=True,
                created_at=datetime.now(timezone.utc),
                update_at = None
            )
            session.add(admin_user)
            await session.commit()
            log.info("Админ создан!!!")
        else:
            log.info("Админ был создан!!!")


if __name__ == "__main__":
    from anyio import run

    run(command)
