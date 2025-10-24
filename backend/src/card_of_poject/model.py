from datetime import datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import TYPE_CHECKING
from uuid import uuid4, UUID as PyUUID

from pytz import timezone
from sqlalchemy import (
    JSON,
    UUID,
    ForeignKey,
    Integer,
    String,
    Text,
    Date,
    # JSON,
    TIMESTAMP,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.core.auth.models import User
from backend.src.core.models.common import BaseTimeMixin
from backend.src.core.models.id import BaseUUIDMixin
from backend.src.core.models.role import Role
from backend.src.models import Base

if TYPE_CHECKING:
    from typing import List


class ProjectStatus(str, Enum):
    # Можно расширить по необходимости
    pass  # или явно указать: DRAFT = "draft", etc.


class Project(Base, BaseUUIDMixin, BaseTimeMixin):

    name: Mapped[str] = mapped_column(String, nullable=False)
    inn: Mapped[str] = mapped_column(String, nullable=True)
    service_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("services.oid"), nullable=False
    )
    manager_id: Mapped[PyUUID] = mapped_column(ForeignKey("users.oid"), nullable=False)
    stage_id: Mapped[PyUUID] = mapped_column(ForeignKey("stages.oid"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    probability: Mapped[Decimal] = mapped_column(
        "probability", nullable=True
    )  # Для выручки с учётом вероятности

    # Связи
    service: Mapped["Service"] = relationship("Service", back_populates="projects")
    manager: Mapped["User"] = relationship("User", back_populates="managed_projects")
    stage: Mapped["Stage"] = relationship("Stage", back_populates="projects")
    financialperiods: Mapped[List["FinancialPeriod"]] = relationship(
        "FinancialPeriod", back_populates="project", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="project", cascade="all, delete-orphan"
    )
    history: Mapped[List["ProjectHistory"]] = relationship(
        "ProjectHistory", back_populates="project", cascade="all, delete-orphan"
    )
    predictions: Mapped[List["ProjectPrediction"]] = relationship(
        "ProjectPrediction", back_populates="project", cascade="all, delete-orphan"
    )

    organization_name: Mapped[str] = mapped_column(String, nullable=False)
    payment_type_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("payment_types.oid"), nullable=True
    )
    business_segment_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("business_segments.oid"), nullable=True
    )
    implementation_year: Mapped[int] = mapped_column(nullable=True)  # Год реализации

    # Флаги
    is_industry_solution: Mapped[bool] = mapped_column(default=False)
    is_forecast_accepted: Mapped[bool] = mapped_column(default=False)
    is_dzo_implementation: Mapped[bool] = mapped_column(default=False)
    requires_management_control: Mapped[bool] = mapped_column(default=False)

    # Условные поля
    accepted_for_evaluation_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("evaluation_types.oid"), nullable=True
    )
    industry_manager: Mapped[str] = mapped_column(String, nullable=True)
    project_number: Mapped[str] = mapped_column(String, nullable=True)

    # Дополнительная информация
    current_status: Mapped[str] = mapped_column(Text, nullable=True)
    completed_this_period: Mapped[str] = mapped_column(Text, nullable=True)
    plans_next_period: Mapped[str] = mapped_column(Text, nullable=True)


class Stage(Base, BaseUUIDMixin):

    stage_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Связи
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="stage")


class Service(Base, BaseUUIDMixin):

    service_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Связи
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="service"
    )


class FinancialPeriod(Base, BaseUUIDMixin, BaseTimeMixin):

    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)  # 1-12
    revenue: Mapped[Decimal] = mapped_column(nullable=True)
    costs: Mapped[Decimal] = mapped_column(nullable=True)

    # Связи
    project: Mapped["Project"] = relationship(
        "Project", back_populates="financialperiods"
    )

    revenue_status_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("revenue_status.oid"), nullable=True
    )
    cost_type_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("cost_types.oid"), nullable=True
    )
    cost_status_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("cost_status.oid"), nullable=True
    )


class Comment(Base, BaseUUIDMixin, BaseTimeMixin):

    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    user_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Связи
    project: Mapped["Project"] = relationship("Project", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")


class ProjectHistory(Base, BaseUUIDMixin):

    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    user_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False, index=True
    )
    field_changed: Mapped[str] = mapped_column(String, nullable=False)
    old_value: Mapped[str] = mapped_column(Text, nullable=True)
    new_value: Mapped[str] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(
            timezone.utc
        ),  # INFO: изменить на datetime.now(timezone.utc)
    )

    # Связи
    project: Mapped["Project"] = relationship("Project", back_populates="history")
    changed_by: Mapped["User"] = relationship("User", back_populates="history_entries")


class Report(Base, BaseUUIDMixin, BaseTimeMixin):

    name: Mapped[str] = mapped_column(String, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_by: Mapped[PyUUID] = mapped_column(ForeignKey("users.oid"), nullable=False)

    # Связи
    created_by_user: Mapped["User"] = relationship("User", back_populates="reports")


class Dashboard(Base, BaseUUIDMixin, BaseTimeMixin):

    name: Mapped[str] = mapped_column(String, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_by: Mapped[PyUUID] = mapped_column(ForeignKey("users.oid"), nullable=False)

    # Связи
    created_by_user: Mapped["User"] = relationship("User", back_populates="dashboards")


class ProjectPrediction(Base, BaseUUIDMixin, BaseTimeMixin):

    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    probability: Mapped[Decimal] = mapped_column(nullable=False)
    predicted_revenue: Mapped[Decimal] = mapped_column(nullable=False)
    forecast_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(
            timezone.utc
        ),  # INFO: изменить на datetime.now(timezone.utc)
    )

    # Связи
    project: Mapped["Project"] = relationship("Project", back_populates="predictions")


class Stage(Base, BaseUUIDMixin):
    stage_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    probability: Mapped[Decimal] = mapped_column(nullable=False)


class PaymentType(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class BusinessSegment(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class EvaluationType(Base, BaseUUIDMixin):  # Принимаемый к оценке
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class CostType(Base, BaseUUIDMixin):  # Вид затрат
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class RevenueStatus(Base, BaseUUIDMixin):  # Статус начисления выручки
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class CostStatus(Base, BaseUUIDMixin):  # Статус отражения затрат
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
