__all__ = ["router"]
from datetime import datetime, timezone
from typing import List
from uuid import uuid4
from uuid import UUID as PyUUID
from fastapi import APIRouter
from src.card_of_poject.model import Comment
from src.card_of_poject.schemas.comment import CommentCreate, CommentResponse
from src.core.auth.current import DepCurrentUser
from src.core.exceptions import InsufficientPermissionsError, ResourceNotFoundError
from src.core.models.role import Role
from src.dependency import DepCommentRep, DepProjectRep


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=CommentResponse,
)
async def create_comment(
    comment: CommentCreate,
    comment_repo: DepCommentRep,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
):
    user_oid, user_role = user_data
    project = await project_repo.get(comment.project_id)
    if user_role == Role.MANAGER and project.manager_id != user_oid:
        raise InsufficientPermissionsError()
    if not project:
        raise ResourceNotFoundError()
    oid = uuid4()

    comment_data = Comment(
        oid=oid,
        **comment.model_dump(),
        created_at=datetime.now(timezone.utc),
    )
    created_comment = await comment_repo.add(comment_data)
    return created_comment


@router.get("/project/{project_id}", response_model=List[CommentResponse])
async def list_comments(
    project_id: PyUUID,
    comment_repo: DepCommentRep,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
):
    user_oid, user_role = user_data

    project = await project_repo.get(project_id)
    if not project:
        raise ResourceNotFoundError()
    if user_role == Role.MANAGER and project.manager_id != user_oid:
        raise InsufficientPermissionsError()
    comments = await comment_repo.list_for_project(project_id)
    return comments


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: PyUUID,
    comment_repo: DepCommentRep,
    user_data: DepCurrentUser,
    project_repo: DepProjectRep,
):
    user_oid, user_role = user_data

    comment = await comment_repo.get(comment_id)
    if not comment:
        raise ResourceNotFoundError()
    project = await project_repo.get(comment.project_id)
    if user_role == Role.MANAGER and project.manager_id != user_oid:
        raise InsufficientPermissionsError()
    await comment_repo.delete(comment_id)
    return {"message": "Comment deleted"}
