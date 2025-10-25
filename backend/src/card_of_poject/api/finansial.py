from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import FinancialPeriodRepository
from schemas import (
    FinancialPeriodCreate,
    FinancialPeriodUpdate,
    FinancialPeriodResponse,
    FinancialPeriodGanttResponse,
)
from models import FinancialPeriod
from database import get_session, require_role
from core.models.role import Role
from uuid import UUID as PyUUID
from typing import List, Optional

router = APIRouter(prefix="/financial-periods", tags=["Financial Periods"])


@router.post(
    "/",
    response_model=FinancialPeriodResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_financial_period(
    period: FinancialPeriodCreate, session: AsyncSession = Depends(get_session)
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    period_data = FinancialPeriod(**period.dict())
    created_period = await repo.add(period_data)
    return created_period


@router.get(
    "/{period_id}",
    response_model=FinancialPeriodResponse,
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_financial_period(
    period_id: PyUUID, session: AsyncSession = Depends(get_session)
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    period = await repo.get(period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Financial period not found")
    return period


@router.put(
    "/{period_id}",
    response_model=FinancialPeriodResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def update_financial_period(
    period_id: PyUUID,
    period: FinancialPeriodUpdate,
    session: AsyncSession = Depends(get_session),
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    existing_period = await repo.get(period_id)
    if not existing_period:
        raise HTTPException(status_code=404, detail="Financial period not found")
    update_data = period.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_period, key, value)
    updated_period = await repo.add(existing_period)
    return updated_period


@router.delete("/{period_id}", dependencies=[Depends(require_role(Role.MANAGER))])
async def delete_financial_period(
    period_id: PyUUID, session: AsyncSession = Depends(get_session)
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    period = await repo.get(period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Financial period not found")
    await repo.delete(period_id)
    return {"message": "Financial period deleted"}


@router.get(
    "/project/{project_id}",
    response_model=List[FinancialPeriodResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def list_financial_periods(
    project_id: PyUUID,
    type: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    periods = await repo.list_for_project(project_id, type)
    return periods


@router.get(
    "/project/{project_id}/gantt",
    response_model=List[FinancialPeriodGanttResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_gantt_periods(
    project_id: PyUUID, type: str, session: AsyncSession = Depends(get_session)
):
    repo = FinancialPeriodRepository(session, FinancialPeriod)
    if type not in ["revenue", "costs"]:
        raise HTTPException(status_code=400, detail="Type must be 'revenue' or 'costs'")
    periods = await repo.get_periods(project_id, type)
    return periods
