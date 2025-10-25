from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.auth.current import get_current_user
from repository import CommentRepository, ProjectRepository
from schemas import CommentCreate, CommentResponse
from models import Comment, Project
from database import get_session
from core.models.role import Role
from uuid import UUID as PyUUID
from typing import List
from models import User

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=CommentResponse,
    dependencies=[Depends(require_role(Role.MANAGER))],
)
async def create_comment(
    comment: CommentCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = CommentRepository(session, Comment)
    project = await ProjectRepository(session, Project).get(comment.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.MANAGER and project.manager_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    comment_data = Comment(**comment.dict())
    created_comment = await repo.add(comment_data)
    return created_comment


@router.get("/project/{project_id}", response_model=List[CommentResponse])
async def list_comments(
    project_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = CommentRepository(session, Comment)
    project = await ProjectRepository(session, Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.MANAGER and project.manager_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    comments = await repo.list_for_project(project_id)
    return comments


@router.delete("/{comment_id}", dependencies=[Depends(require_role(Role.MANAGER))])
async def delete_comment(
    comment_id: PyUUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = CommentRepository(session, Comment)
    comment = await repo.get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    project = await ProjectRepository(session, Project).get(comment.project_id)
    if user.role == Role.MANAGER and project.manager_id != user.oid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    await repo.delete(comment_id)
    return {"message": "Comment deleted"}
