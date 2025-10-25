from pydantic import BaseModel
from uuid import UUID as PyUUID
from typing import Optional
from datetime import datetime


class ProjectPredictionBase(BaseModel):
    project_id: PyUUID
    probability: float
    predicted_revenue: float


class ProjectPredictionCreate(ProjectPredictionBase):
    pass


class ProjectPredictionResponse(ProjectPredictionBase):
    oid: PyUUID
    calculated_at: datetime

    class Config:
        orm_mode = True
