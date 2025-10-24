from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


class BaseTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
