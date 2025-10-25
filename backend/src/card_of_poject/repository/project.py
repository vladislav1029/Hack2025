from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import selectinload

from sqlalchemy import func, select
from backend.src.card_of_poject.model import (
    BusinessSegment,
    FinancialPeriod,
    Project,
    ProjectHistory,
    Service,
    Stage,
)
from backend.src.card_of_poject.repository.base_repository import BaseRepository, IDType
from backend.src.core.auth.models import User


class ProjectRepository(BaseRepository[Project]):
    async def get(self, id: IDType) -> Optional[Project]:
        query = (
            select(Project)
            .where(Project.oid == id)
            .options(
                selectinload(Project.service),
                selectinload(Project.manager),
                selectinload(Project.stage),
                selectinload(Project.financialperiods),
                selectinload(Project.comments),
                selectinload(Project.history),
                selectinload(Project.predictions),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list(self, filters: Optional[dict] = None) -> List[Project]:
        query = select(Project).options(
            selectinload(Project.service),
            selectinload(Project.manager),
            selectinload(Project.stage),
            selectinload(Project.financialperiods),
        )
        if filters:
            if "stage_id" in filters:
                query = query.where(Project.stage_id == filters["stage_id"])
            if "manager_id" in filters:
                query = query.where(Project.manager_id == filters["manager_id"])
            if "business_segment_id" in filters:
                query = query.where(
                    Project.business_segment_id == filters["business_segment_id"]
                )
            if "service_id" in filters:
                query = query.where(Project.service_id == filters["service_id"])
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_analytics(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict:
        # Общее кол-во и выручка
        query_total = select(func.count()).select_from(Project)
        query_revenue = select(func.sum(FinancialPeriod.revenue)).where(
            FinancialPeriod.revenue.isnot(None)
        )

        # По стадиям, менеджерам, услугам, сегментам
        query_by_stage = (
            select(Project.stage_id, Stage.stage_name, func.count())
            .join(Stage)
            .group_by(Project.stage_id, Stage.stage_name)
        )
        query_by_manager = (
            select(Project.manager_id, User.name, func.count())
            .join(User)
            .group_by(Project.manager_id, User.name)
        )
        query_by_service = (
            select(Project.service_id, Service.service_name, func.count())
            .join(Service)
            .group_by(Project.service_id, Service.service_name)
        )
        query_by_segment = (
            select(Project.business_segment_id, BusinessSegment.name, func.count())
            .join(BusinessSegment)
            .group_by(Project.business_segment_id, BusinessSegment.name)
        )

        # Сумма по менеджерам/сегментам/услугам
        query_revenue_by_manager = (
            select(Project.manager_id, User.name, func.sum(FinancialPeriod.revenue))
            .join(FinancialPeriod)
            .join(User)
            .where(FinancialPeriod.revenue.isnot(None))
            .group_by(Project.manager_id, User.name)
        )
        query_revenue_by_segment = (
            select(
                Project.business_segment_id,
                BusinessSegment.name,
                func.sum(FinancialPeriod.revenue),
            )
            .join(FinancialPeriod)
            .join(BusinessSegment)
            .where(FinancialPeriod.revenue.isnot(None))
            .group_by(Project.business_segment_id, BusinessSegment.name)
        )
        query_revenue_by_service = (
            select(
                Project.service_id,
                Service.service_name,
                func.sum(FinancialPeriod.revenue),
            )
            .join(FinancialPeriod)
            .join(Service)
            .where(FinancialPeriod.revenue.isnot(None))
            .group_by(Project.service_id, Service.service_name)
        )

        # Среднее время на стадии
        query_avg_stage_time = (
            select(
                ProjectHistory.new_value,
                Stage.stage_name,
                func.avg(
                    ProjectHistory.changed_at
                    - func.lag(ProjectHistory.changed_at).over(
                        partition_by=ProjectHistory.project_id,
                        order_by=ProjectHistory.changed_at,
                    )
                ).label("avg_time"),
            )
            .join(Stage, ProjectHistory.new_value == Stage.oid)
            .where(ProjectHistory.field_changed == "stage_id")
            .group_by(ProjectHistory.new_value, Stage.stage_name)
        )

        # Выручка с учетом вероятности
        query_weighted_revenue = (
            select(Project.oid, func.sum(FinancialPeriod.revenue * Project.probability))
            .join(FinancialPeriod)
            .where(FinancialPeriod.revenue.isnot(None))
            .group_by(Project.oid)
        )

        total = (await self.session.execute(query_total)).scalar() or 0
        revenue = (await self.session.execute(query_revenue)).scalar() or 0
        by_stage = (await self.session.execute(query_by_stage)).all()
        by_manager = (await self.session.execute(query_by_manager)).all()
        by_service = (await self.session.execute(query_by_service)).all()
        by_segment = (await self.session.execute(query_by_segment)).all()
        revenue_by_manager = (
            await self.session.execute(query_revenue_by_manager)
        ).all()
        revenue_by_segment = (
            await self.session.execute(query_revenue_by_segment)
        ).all()
        revenue_by_service = (
            await self.session.execute(query_revenue_by_service)
        ).all()
        avg_stage_time = (await self.session.execute(query_avg_stage_time)).all()
        weighted_revenue = (await self.session.execute(query_weighted_revenue)).all()

        return {
            "total_projects": total,
            "total_revenue": float(revenue),
            "by_stage": [
                {"stage_id": s[0], "stage_name": s[1], "count": s[2]} for s in by_stage
            ],
            "by_manager": [
                {"manager_id": m[0], "manager_name": m[1], "count": m[2]}
                for m in by_manager
            ],
            "by_service": [
                {"service_id": s[0], "service_name": s[1], "count": s[2]}
                for s in by_service
            ],
            "by_segment": [
                {"segment_id": s[0], "segment_name": s[1], "count": s[2]}
                for s in by_segment
            ],
            "revenue_by_manager": [
                {"manager_id": m[0], "manager_name": m[1], "revenue": float(m[2] or 0)}
                for m in revenue_by_manager
            ],
            "revenue_by_segment": [
                {"segment_id": s[0], "segment_name": s[1], "revenue": float(s[2] or 0)}
                for s in revenue_by_segment
            ],
            "revenue_by_service": [
                {"service_id": s[0], "service_name": s[1], "revenue": float(s[2] or 0)}
                for s in revenue_by_service
            ],
            "avg_stage_time": [
                {
                    "stage_id": t[0],
                    "stage_name": t[1],
                    "avg_days": t[2].total_seconds() / 86400 if t[2] else 0,
                }
                for t in avg_stage_time
            ],
            "weighted_revenue_by_project": [
                {"project_id": w[0], "weighted_revenue": float(w[1] or 0)}
                for w in weighted_revenue
            ],
        }
