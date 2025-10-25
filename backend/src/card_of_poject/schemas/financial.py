from pydantic import BaseModel, field_validator
from uuid import UUID as PyUUID
from typing import Optional
from .references import RevenueStatusResponse, CostTypeResponse, CostStatusResponse


class FinancialPeriodBase(BaseModel):
    project_id: PyUUID
    year: int
    month: int
    revenue: Optional[float] = None
    costs: Optional[float] = None
    revenue_status_id: Optional[PyUUID] = None
    cost_type_id: Optional[PyUUID] = None
    cost_status_id: Optional[PyUUID] = None

    @field_validator("revenue_status_id")
    def check_revenue_status(cls, v, values):
        if values.get("revenue") is not None and not v:
            raise ValueError("revenue_status_id required when revenue is set")
        return v

    @field_validator("cost_type_id", "cost_status_id")
    def check_cost_fields(cls, v, values, field):
        if values.get("costs") is not None and not v:
            raise ValueError(f"{field.name} required when costs is set")
        return v


class FinancialPeriodCreate(FinancialPeriodBase):
    pass


class FinancialPeriodUpdate(FinancialPeriodBase):
    project_id: Optional[PyUUID] = None
    year: Optional[int] = None
    month: Optional[int] = None


class FinancialPeriodResponse(FinancialPeriodBase):
    oid: PyUUID
    revenue_status: Optional[RevenueStatusResponse]
    cost_type: Optional[CostTypeResponse]
    cost_status: Optional[CostStatusResponse]

    class Config:
        orm_mode = True


class FinancialPeriodGanttResponse(BaseModel):
    year: int
    month: int
    amount: float
    status: str
    cost_type: Optional[str]

    class Config:
        orm_mode = True
