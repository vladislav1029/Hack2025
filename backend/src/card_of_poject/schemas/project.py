from pydantic import BaseModel, field_validator
from uuid import UUID as PyUUID
from typing import Optional, List, Dict, Union
from datetime import datetime

from src.card_of_poject.schemas.base import ReferenceResponse
from .references import StageResponse, ServiceResponse, BusinessSegmentResponse
from repository.financila import FinancialPeriodResponse
from repository.history import ProjectHistoryResponse
from repository.references import CommentResponse
from repository.base_repository import ProjectPredictionResponse


class ProjectBase(BaseModel):
    name: str
    organization_name: str
    inn: Optional[str] = None
    service_id: PyUUID
    manager_id: PyUUID
    stage_id: PyUUID
    payment_type_id: PyUUID
    business_segment_id: PyUUID
    implementation_year: Optional[int] = None
    is_industry_solution: bool = False
    is_forecast_accepted: bool = False
    is_dzo_implementation: bool = False
    requires_management_control: bool = False
    accepted_for_evaluation_id: Optional[PyUUID] = None
    industry_manager: Optional[str] = None
    project_number: Optional[str] = None
    current_status: Optional[str] = None
    completed_this_period: Optional[str] = None
    plans_next_period: Optional[str] = None
    probability: Optional[float] = None

    @field_validator("accepted_for_evaluation_id")
    def check_evaluation(cls, v, values):
        if values.get("is_forecast_accepted") and not v:
            raise ValueError(
                "accepted_for_evaluation_id required when is_forecast_accepted is True"
            )
        return v

    @field_validator("industry_manager")
    def check_industry_manager(cls, v, values):
        if values.get("is_industry_solution") and not v:
            raise ValueError(
                "industry_manager required when is_industry_solution is True"
            )
        return v


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    organization_name: Optional[str] = None
    service_id: Optional[PyUUID] = None
    manager_id: Optional[PyUUID] = None
    stage_id: Optional[PyUUID] = None
    payment_type_id: Optional[PyUUID] = None
    business_segment_id: Optional[PyUUID] = None


class ProjectResponse(ProjectBase):
    oid: PyUUID
    created_at: datetime
    updated_at: Optional[datetime]
    service: ServiceResponse
    manager: ReferenceResponse
    stage: StageResponse
    business_segment: BusinessSegmentResponse
    financial_periods: List[FinancialPeriodResponse]
    history: List[ProjectHistoryResponse]
    comments: List[CommentResponse]
    predictions: List[ProjectPredictionResponse]

    class Config:
        orm_mode = True


class ProjectRegistryResponse(BaseModel):
    project_id: PyUUID
    segment: Optional[str]
    inn: Optional[str]
    organization_name: str
    name: str
    stage: str
    implementation_year: Optional[int]
    service: str
    manager: str
    total_revenue: float
    weighted_revenue: float
    changes: List[str]

    class Config:
        orm_mode = True


class AnalyticsResponse(BaseModel):
    total_projects: int
    total_revenue: float
    by_stage: List[Dict[str, Union[PyUUID, str, int]]]
    by_manager: List[Dict[str, Union[PyUUID, str, int]]]
    by_service: List[Dict[str, Union[PyUUID, str, int]]]
    by_segment: List[Dict[str, Union[PyUUID, str, int]]]
    revenue_by_manager: List[Dict[str, Union[PyUUID, str, float]]]
    revenue_by_segment: List[Dict[str, Union[PyUUID, str, float]]]
    revenue_by_service: List[Dict[str, Union[PyUUID, str, float]]]
    avg_stage_time: List[Dict[str, Union[PyUUID, str, float]]]
    weighted_revenue_by_project: List[Dict[str, Union[PyUUID, float]]]
