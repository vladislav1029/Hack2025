from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import ProjectHistoryRepository
from schemas import ProjectHistoryCreate, ProjectHistoryResponse, StageChangeResponse
from models import ProjectHistory
from database import get_session, require_role
from core.models.role import Role
from uuid import UUID as PyUUID
from typing import List
from datetime import datetime

router = APIRouter(prefix="/history", tags=["Project History"])


@router.post(
    "/",
    response_model=ProjectHistoryResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_history(
    history: ProjectHistoryCreate, session: AsyncSession = Depends(get_session)
):
    repo = ProjectHistoryRepository(session, ProjectHistory)
    history_data = ProjectHistory(**history.dict())
    created_history = await repo.add(history_data)
    return created_history


@router.get(
    "/project/{project_id}",
    response_model=List[ProjectHistoryResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def list_history(
    project_id: PyUUID, limit: int = 10, session: AsyncSession = Depends(get_session)
):
    repo = ProjectHistoryRepository(session, ProjectHistory)
    history = await repo.get_last_changes(project_id, limit)
    return history


@router.get(
    "/project/{project_id}/stages",
    response_model=List[StageChangeResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_stage_changes(
    project_id: PyUUID, session: AsyncSession = Depends(get_session)
):
    repo = ProjectHistoryRepository(session, ProjectHistory)
    stage_changes = await repo.get_stage_changes(project_id)
    return stage_changes


@router.get(
    "/period",
    response_model=List[ProjectHistoryResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def list_history_for_period(
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectHistoryRepository(session, ProjectHistory)
    history = await repo.list_for_period(start_date, end_date)
    return history
