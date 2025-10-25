from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import ProjectRepository, StageRepository
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectRegistryResponse,
    AnalyticsResponse,
)
from models import Project, Stage
from database import get_async_session
from core.models.role import Role
from uuid import UUID as PyUUID
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
)
async def create_project(
    project: ProjectCreate,
    user_data: DepCurrentUser,
    session: AsyncSession = Depends(get_async_session),
):
    repo = ProjectRepository(session, Project)
    stage_repo = StageRepository(session, Stage)
    stage = await stage_repo.get(project.stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    project_data = Project(**project.dict())
    project_data.probability = stage.probability
    created_project = await repo.add(project_data)
    return created_project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_project(
    project_id: PyUUID, session: AsyncSession = Depends(get_async_session)
):
    repo = ProjectRepository(session, Project)
    project = await repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def update_project(
    project_id: PyUUID,
    project: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    repo = ProjectRepository(session, Project)
    stage_repo = StageRepository(session, Stage)
    existing_project = await repo.get(project_id)
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = project.dict(exclude_unset=True)
    if "stage_id" in update_data:
        stage = await stage_repo.get(update_data["stage_id"])
        if not stage:
            raise HTTPException(status_code=404, detail="Stage not found")
        update_data["probability"] = stage.probability
    for key, value in update_data.items():
        setattr(existing_project, key, value)
    updated_project = await repo.add(existing_project)
    return updated_project


@router.delete("/{project_id}", dependencies=[Depends(require_role(Role.MANAGER))])
async def delete_project(
    project_id: PyUUID, session: AsyncSession = Depends(get_async_session)
):
    repo = ProjectRepository(session, Project)
    project = await repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await repo.delete(project_id)
    return {"message": "Project deleted"}


@router.get(
    "/",
    response_model=List[ProjectResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def list_projects(
    stage_id: Optional[PyUUID] = None,
    manager_id: Optional[PyUUID] = None,
    business_segment_id: Optional[PyUUID] = None,
    service_id: Optional[PyUUID] = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = ProjectRepository(session, Project)
    filters = {}
    if stage_id:
        filters["stage_id"] = stage_id
    if manager_id:
        filters["manager_id"] = manager_id
    if business_segment_id:
        filters["business_segment_id"] = business_segment_id
    if service_id:
        filters["service_id"] = service_id
    projects = await repo.list(filters)
    return projects


@router.get(
    "/registry",
    response_model=List[ProjectRegistryResponse],
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_project_registry(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = ProjectRepository(session, Project)
    registry = await repo.get_project_registry(start_date, end_date)
    return registry


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
    dependencies=[Depends(require_role(Role.USER))],
)
async def get_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = ProjectRepository(session, Project)
    analytics = await repo.get_analytics(start_date, end_date)
    return analytics
