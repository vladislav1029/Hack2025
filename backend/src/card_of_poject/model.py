from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID as PyUUID


from sqlalchemy import (
    JSON,
    UUID,
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Date,
    # JSON,
    TIMESTAMP,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.common import BaseTimeMixin
from src.core.models.id import BaseUUIDMixin
from src.models import Base

if TYPE_CHECKING:
    from src.core.auth.models import User


# === СПРАВОЧНИКИ ===
class Service(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="service"
    )


class PaymentType(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="payment_type"
    )


class Stage(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    probability: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=0.0
    )
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="stage")


class BusinessSegment(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="business_segment"
    )


class EvaluationType(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="accepted_for_evaluation"
    )


class CostType(Base, BaseUUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    financial_periods: Mapped[List["FinancialPeriod"]] = relationship(
        "FinancialPeriod", back_populates="cost_type"
    )


class RevenueStatus(Base, BaseUUIDMixin):

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    financial_periods: Mapped[List["FinancialPeriod"]] = relationship(
        "FinancialPeriod", back_populates="revenue_status"
    )


class CostStatus(Base, BaseUUIDMixin):

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    financial_periods: Mapped[List["FinancialPeriod"]] = relationship(
        "FinancialPeriod", back_populates="cost_status"
    )


# === ОСНОВНЫЕ СУЩНОСТИ ===
class Project(Base, BaseUUIDMixin, BaseTimeMixin):
    # === Общая информация ===
    organization_name: Mapped[str] = mapped_column(String(500), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)

    service_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("services.oid"), nullable=False
    )
    payment_type_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("payment_types.oid"), nullable=True
    )
    stage_id: Mapped[PyUUID] = mapped_column(ForeignKey("stages.oid"), nullable=False)
    manager_id: Mapped[PyUUID] = mapped_column(ForeignKey("users.oid"), nullable=False)
    business_segment_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("business_segments.oid"), nullable=True
    )
    implementation_year: Mapped[int] = mapped_column(Integer, nullable=True)

    # === Флаги ===
    is_industry_solution: Mapped[bool] = mapped_column(Boolean, default=False)
    is_forecast_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_dzo_implementation: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_management_control: Mapped[bool] = mapped_column(Boolean, default=False)

    # === Условные поля ===
    accepted_for_evaluation_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("evaluation_types.oid"), nullable=True
    )
    industry_manager: Mapped[str] = mapped_column(String(255), nullable=True)
    project_number: Mapped[str] = mapped_column(String(100), nullable=True)

    # === Даты ===
    created_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False, default=func.current_date()
    )

    # === Дополнительно ===
    current_status: Mapped[str] = mapped_column(Text, nullable=True)
    completed_this_period: Mapped[str] = mapped_column(Text, nullable=True)
    plans_next_period: Mapped[str] = mapped_column(Text, nullable=True)

    # === Связи ===
    service: Mapped["Service"] = relationship("Service", back_populates="projects")
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", back_populates="projects"
    )
    stage: Mapped["Stage"] = relationship("Stage", back_populates="projects")
    manager: Mapped["User"] = relationship(
        "User",
        back_populates="managed_projects",
        foreign_keys=[manager_id],  # Правильно: передаём объект колонки
    )
    business_segment: Mapped["BusinessSegment"] = relationship(
        "BusinessSegment", back_populates="projects"
    )
    accepted_for_evaluation: Mapped["EvaluationType"] = relationship(
        "EvaluationType", back_populates="projects"
    )

    financial_periods: Mapped[List["FinancialPeriod"]] = relationship(
        "FinancialPeriod", back_populates="project", cascade="all, delete-orphan"
    )
    history: Mapped[List["ProjectHistory"]] = relationship(
        "ProjectHistory", back_populates="project", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="project", cascade="all, delete-orphan"
    )
    predictions: Mapped[List["ProjectPrediction"]] = relationship(
        "ProjectPrediction", back_populates="project", cascade="all, delete-orphan"
    )


class FinancialPeriod(Base, BaseUUIDMixin, BaseTimeMixin):
    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)

    revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    revenue_status_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("revenue_status.oid"), nullable=True
    )
    costs: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    cost_type_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("cost_types.oid"), nullable=True
    )
    cost_status_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("cost_status.oid"), nullable=True
    )

    project: Mapped["Project"] = relationship(
        "Project", back_populates="financial_periods"
    )
    revenue_status: Mapped["RevenueStatus"] = relationship(
        "RevenueStatus", back_populates="financial_periods"
    )
    cost_type: Mapped["CostType"] = relationship(
        "CostType", back_populates="financial_periods"
    )
    cost_status: Mapped["CostStatus"] = relationship(
        "CostStatus", back_populates="financial_periods"
    )


class ProjectHistory(Base, BaseUUIDMixin):
    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    user_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False, index=True
    )
    field_changed: Mapped[str] = mapped_column(String(255), nullable=False)
    old_value: Mapped[str] = mapped_column(Text, nullable=True)
    new_value: Mapped[str] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    project: Mapped["Project"] = relationship("Project", back_populates="history")
    changed_by: Mapped["User"] = relationship("User", back_populates="history_entries")


class Comment(Base, BaseUUIDMixin, BaseTimeMixin):
    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    user_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")


class Report(Base, BaseUUIDMixin, BaseTimeMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_by_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False
    )

    created_by: Mapped["User"] = relationship("User", back_populates="reports")


class Dashboard(Base, BaseUUIDMixin, BaseTimeMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_by_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.oid"), nullable=False
    )

    created_by: Mapped["User"] = relationship("User", back_populates="dashboards")


class ProjectPrediction(Base, BaseUUIDMixin, BaseTimeMixin):
    project_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("projects.oid"), nullable=False, index=True
    )
    predicted_revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    probability: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    forecast_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    project: Mapped["Project"] = relationship("Project", back_populates="predictions")
