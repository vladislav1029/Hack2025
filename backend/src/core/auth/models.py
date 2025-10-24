from datetime import datetime
from typing import List
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from backend.src.card_of_poject.model import (
    Comment,
    Dashboard,
    Project,
    ProjectHistory,
    Report,
)
from src.core.models import BaseUUIDMixin, BaseTimeMixin, Role
from src.models import Base

# INFO: Стоило бы писать в стиле DDD но это overkill для этого. Также использование привязки к postgresql это ограничение.


class User(Base, BaseUUIDMixin, BaseTimeMixin):

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verificate: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[Role] = mapped_column(Integer, default=2, nullable=False)

    managed_projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="manager", foreign_keys="Project.manager_id"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
    history_entries: Mapped[List["ProjectHistory"]] = relationship(
        "ProjectHistory", back_populates="changed_by"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report", back_populates="created_by_user"
    )
    dashboards: Mapped[List["Dashboard"]] = relationship(
        "Dashboard", back_populates="created_by_user"
    )


class RefreshToken(Base, BaseUUIDMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.oid"), index=True)
    expired_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
