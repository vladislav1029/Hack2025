from sqlalchemy import select
from src.card_of_poject.repository.base_repository import BaseRepository
from models import FinancialPeriod, RevenueStatus, CostType, CostStatus
from typing import Dict, List, Optional
from uuid import UUID as PyUUID
from sqlalchemy.orm import selectinload


class FinancialPeriodRepository(BaseRepository[FinancialPeriod]):
    async def get(self, id: PyUUID) -> Optional[FinancialPeriod]:
        query = (
            select(FinancialPeriod)
            .where(FinancialPeriod.oid == id)
            .options(
                selectinload(FinancialPeriod.project),
                selectinload(FinancialPeriod.revenue_status),
                selectinload(FinancialPeriod.cost_type),
                selectinload(FinancialPeriod.cost_status),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list_for_project(
        self, project_id: PyUUID, type: Optional[str] = None
    ) -> List[FinancialPeriod]:
        query = (
            select(FinancialPeriod)
            .where(FinancialPeriod.project_id == project_id)
            .options(
                selectinload(FinancialPeriod.revenue_status),
                selectinload(FinancialPeriod.cost_type),
                selectinload(FinancialPeriod.cost_status),
            )
        )
        if type == "revenue":
            query = query.where(FinancialPeriod.revenue.isnot(None))
        elif type == "costs":
            query = query.where(FinancialPeriod.costs.isnot(None))
        result = await self.session.execute(query)
        return result.scalars().all()

    # INFO: выручка и затраты для Ганта

    async def get_periods(self, project_id: PyUUID, type: str) -> List[Dict]:
        query = (
            select(FinancialPeriod)
            .where(FinancialPeriod.project_id == project_id)
            .options(
                selectinload(FinancialPeriod.revenue_status),
                selectinload(FinancialPeriod.cost_type),
                selectinload(FinancialPeriod.cost_status),
            )
        )
        if type == "revenue":
            query = query.where(FinancialPeriod.revenue.isnot(None))
        elif type == "costs":
            query = query.where(FinancialPeriod.costs.isnot(None))
        result = await self.session.execute(query)
        periods = result.scalars().all()
        return [
            {
                "year": p.year,
                "month": p.month,
                "amount": float(p.revenue or p.costs),
                "status": (
                    p.revenue_status.name if type == "revenue" else p.cost_status.name
                ),
                "cost_type": p.cost_type.name if type == "costs" else None,
            }
            for p in periods
        ]
