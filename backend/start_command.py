from datetime import datetime, timezone
import uuid

from anyio import run
from src.core.models.role import Role
from src.core.reposiory import UserRepository
from src.database import session_maker
from src.dependensy import get_password_hasher
from src.core.auth.models import User
from src.config import settings
import structlog

log = structlog.get_logger()


async def command():

    hasher = get_password_hasher()
    user_id = uuid.uuid4()
    password = hasher.hash_password(settings.admin.password)
    async with session_maker() as session:
        repo = UserRepository(session=session)
        model = User(
            oid=user_id,
            email=settings.admin.mail,
            password=password,
            created_at=datetime.now(timezone.utc),
            update_at=None,
            role=Role.ADMIN,
        )
        await repo.add(model)
    log.info("Админ создан!!!")


if __name__ == "__main__":
    run(command)
