from pydantic import BaseModel
from uuid import UUID as PyUUID
from typing import  Dict
from datetime import datetime

from src.card_of_poject.schemas.base import ReferenceResponse


class ReportBase(BaseModel):
    name: str
    config: Dict
    created_by: PyUUID


class ReportCreate(ReportBase):
    pass


class ReportResponse(ReportBase):
    oid: PyUUID
    created_at: datetime
    creator: ReferenceResponse  # User.name

    class Config:
        from_attributes = True


class DashboardBase(BaseModel):
    name: str
    config: Dict
    created_by: PyUUID


class DashboardCreate(DashboardBase):
    pass


class DashboardResponse(DashboardBase):
    oid: PyUUID
    created_at: datetime
    creator: ReferenceResponse

    class Config:
        from_attributes = True
