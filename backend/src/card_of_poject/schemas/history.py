from pydantic import BaseModel
from uuid import UUID as PyUUID
from typing import Optional
from datetime import datetime
from .references import ReferenceResponse


class ProjectHistoryBase(BaseModel):
    project_id: PyUUID
    user_id: PyUUID
    field_changed: str
    old_value: Optional[str]
    new_value: Optional[str]


class ProjectHistoryCreate(ProjectHistoryBase):
    pass


class ProjectHistoryResponse(ProjectHistoryBase):
    oid: PyUUID
    changed_at: datetime
    changed_by: ReferenceResponse  # User.name

    class Config:
        orm_mode = True


class StageChangeResponse(BaseModel):
    stage_name: str
    changed_at: datetime

    class Config:
        orm_mode = True
