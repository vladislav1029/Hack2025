from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


from src.core.models import BaseUUIDMixin, BaseTimeMixin, Role
from src.models import Base

# INFO: Стоило бы писать в стиле DDD но это overkill для этого. Также использование привязки к postgresql это ограничение.


class User(Base, BaseUUIDMixin, BaseTimeMixin):

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verificate: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[Role] = mapped_column(Integer, default=0, nullable=False)


class RefreshToken(Base, BaseUUIDMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.oid"), index=True)
    expired_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
