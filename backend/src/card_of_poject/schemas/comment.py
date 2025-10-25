from pydantic import BaseModel
from uuid import UUID as PyUUID
from typing import Optional
from datetime import datetime
from .references import ReferenceResponse


class CommentBase(BaseModel):
    project_id: PyUUID
    user_id: PyUUID
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    oid: PyUUID
    created_at: datetime
    author: ReferenceResponse  # User.name

    class Config:
        orm_mode = True
