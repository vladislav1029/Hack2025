from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.core.auth.current import get_current_user
from repository import ReportRepository, DashboardRepository
from schemas import ReportCreate, ReportResponse, DashboardCreate, DashboardResponse
from models import Report, Dashboard, Role
from uuid import UUID as PyUUID
from typing import List
from models import User
from database import get_session
from core.models.role import Role
from dependencies import require_role

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post(
    "/reports",
    response_model=ReportResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_report(
    report: ReportCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = ReportRepository(session, Report)
    report_data = Report(**report.dict(), created_by=user.oid)
    created_report = await repo.add(report_data)
    return created_report


@router.get("/reports/user/{user_id}", response_model=List[ReportResponse])
async def list_reports(
    user_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = ReportRepository(session, Report)
    if user.role == Role.MANAGER and user_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    reports = await repo.list_by_user(user_id)
    return reports


@router.delete(
    "/reports/{report_id}", dependencies=[Depends(require_role(Role.MANAGER))]
)
async def delete_report(
    report_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = ReportRepository(session, Report)
    report = await repo.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if user.role == Role.MANAGER and report.created_by != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    await repo.delete(report_id)
    return {"message": "Report deleted"}


@router.post(
    "/dashboards",
    response_model=DashboardResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_dashboard(
    dashboard: DashboardCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = DashboardRepository(session, Dashboard)
    dashboard_data = Dashboard(**dashboard.dict(), created_by=user.oid)
    created_dashboard = await repo.add(dashboard_data)
    return created_dashboard


@router.get("/dashboards/user/{user_id}", response_model=List[DashboardResponse])
async def list_dashboards(
    user_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = DashboardRepository(session, Dashboard)
    if user.role == Role.MANAGER and user_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    dashboards = await repo.list_by_user(user_id)
    return dashboards


@router.delete(
    "/dashboards/{dashboard_id}", dependencies=[Depends(require_role(Role.MANAGER))]
)
async def delete_dashboard(
    dashboard_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = DashboardRepository(session, Dashboard)
    dashboard = await repo.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    if user.role == Role.MANAGER and dashboard.created_by != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    await repo.delete(dashboard_id)
    return {"message": "Dashboard deleted"}
