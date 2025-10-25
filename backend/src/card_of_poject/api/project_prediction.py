from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.core.auth.current import get_current_user
from repository import ProjectPredictionRepository, ProjectRepository
from schemas import ProjectPredictionCreate, ProjectPredictionResponse
from models import ProjectPrediction, Project, Role
from uuid import UUID as PyUUID
from typing import Optional
from database import get_session
from core.models.role import Role

# from dependencies import require_role
from models import User

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post(
    "/",
    response_model=ProjectPredictionResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_prediction(
    prediction: ProjectPredictionCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = ProjectPredictionRepository(session, ProjectPrediction)
    project = await ProjectRepository(session, Project).get(prediction.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.MANAGER and project.manager_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    prediction_data = ProjectPrediction(**prediction.dict())
    created_prediction = await repo.add(prediction_data)
    return created_prediction


@router.get(
    "/project/{project_id}/latest", response_model=Optional[ProjectPredictionResponse]
)
async def get_latest_prediction(
    project_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = ProjectPredictionRepository(session, ProjectPrediction)
    project = await ProjectRepository(session, Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.MANAGER and project.manager_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    prediction = await repo.get_latest(project_id)
    return prediction
