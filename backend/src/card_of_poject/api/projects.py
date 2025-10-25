__all__ = ["router"]
from fastapi import APIRouter
from src.card_of_poject.model import Project
from src.card_of_poject.schemas.project import (
    AnalyticsResponse,
    ProjectCreate,
    ProjectRegistryResponse,
    ProjectResponse,
    ProjectUpdate,
)
from src.core.auth.current import DepCurrentUser

from uuid import UUID as PyUUID, uuid4
from typing import List, Optional
from datetime import datetime, timezone

from src.core.exceptions import InsufficientPermissionsError, ResourceNotFoundError
from src.core.models.role import Role
from src.dependency import DepProjectRep, DepStageRep

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
)
async def create_project(
    project: ProjectCreate,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
    stage_repo: DepStageRep,
):
    user_id, user_role = user_data
    if user_role != Role.ADMIN:
        raise InsufficientPermissionsError()
    stage = await stage_repo.get(project.stage_id)
    if not stage:
        raise ResourceNotFoundError()
    oid = uuid4()
    project_data = Project(
        oid=oid,
        **project.model_validate(),
        created_at=datetime.now(timezone.utc),
    )
    project_data.probability = stage.probability
    created_project = await project_repo.add(project_data)
    return created_project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: PyUUID,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
):

    project = await project_repo.get(project_id)
    if not project:
        raise ResourceNotFoundError()
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: PyUUID,
    user_data: DepCurrentUser,
    project: ProjectUpdate,
    project_repo: DepProjectRep,
    stage_repo: DepStageRep,
):
    user_id, user_role = user_data
    if user_role == Role.USER:
        raise InsufficientPermissionsError()

    existing_project = await project_repo.get(project_id)
    if not existing_project:
        raise ResourceNotFoundError()
    update_data = project.model_dump(exclude_unset=True)
    if "stage_id" in update_data:
        stage = await stage_repo.get(update_data["stage_id"])
        if not stage:
            raise ResourceNotFoundError()
        update_data["probability"] = stage.probability
    for key, value in update_data.items():
        setattr(existing_project, key, value)
    update_data["update_at"] = datetime.now(timezone.utc)
    updated_project = await project_repo.add(existing_project)
    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: PyUUID,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
):
    user_id, user_role = user_data
    if user_role == Role.USER:
        raise InsufficientPermissionsError()
    project = await project_repo.get(project_id)
    if not project:
        raise ResourceNotFoundError()
    await project_repo.delete(project_id)
    return {"message": "Project deleted"}


@router.get(
    "/",
    response_model=List[ProjectResponse],
)
async def list_projects(
    project_repo: DepProjectRep,
    stage_id: Optional[PyUUID] = None,
    manager_id: Optional[PyUUID] = None,
    business_segment_id: Optional[PyUUID] = None,
    service_id: Optional[PyUUID] = None,
):
    filters = {}
    if stage_id:
        filters["stage_id"] = stage_id
    if manager_id:
        filters["manager_id"] = manager_id
    if business_segment_id:
        filters["business_segment_id"] = business_segment_id
    if service_id:
        filters["service_id"] = service_id
    projects = await project_repo.list(filters)
    return projects


@router.get(
    "/registry",
    response_model=List[ProjectRegistryResponse],
)
async def get_project_registry(
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):

    registry = await project_repo.get_project_registry(start_date, end_date)
    return registry


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
)
async def get_analytics(
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):

    analytics = await project_repo.get_analytics(start_date, end_date)
    return analytics
