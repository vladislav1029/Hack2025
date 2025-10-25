from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import selectinload

from sqlalchemy import func, select
from backend.src.card_of_poject.model import FinancialPeriod, Project
from backend.src.card_of_poject.repository.base_repository import BaseRepository, IDType


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
    ) -> dict:
        # Аналитика для стартовой страницы
        query_total = select(func.count()).select_from(Project)
        query_revenue = select(func.sum(FinancialPeriod.revenue)).where(
            FinancialPeriod.revenue.isnot(None)
        )
        query_by_stage = select(Project.stage_id, func.count()).group_by(
            Project.stage_id
        )
        query_by_manager = select(Project.manager_id, func.count()).group_by(
            Project.manager_id
        )
        query_by_segment = select(Project.business_segment_id, func.count()).group_by(
            Project.business_segment_id
        )

        total = (await self.session.execute(query_total)).scalar()
        revenue = (await self.session.execute(query_revenue)).scalar() or 0
        by_stage = (await self.session.execute(query_by_stage)).all()
        by_manager = (await self.session.execute(query_by_manager)).all()
        by_segment = (await self.session.execute(query_by_segment)).all()

        return {
            "total_projects": total,
            "total_revenue": float(revenue),
            "by_stage": [{"stage_id": s[0], "count": s[1]} for s in by_stage],
            "by_manager": [{"manager_id": m[0], "count": m[1]} for m in by_manager],
            "by_segment": [{"segment_id": s[0], "count": s[1]} for s in by_segment],
        }
