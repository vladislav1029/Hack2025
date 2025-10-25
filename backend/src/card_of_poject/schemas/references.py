from typing import Optional
from uuid import UUID as PyUUID

from src.card_of_poject.schemas.base import ReferenceBase, ReferenceCreate, ReferenceResponse


class StageBase(ReferenceBase):
    probability: Optional[float] = None


class StageCreate(StageBase):
    pass


class StageResponse(StageBase):
    oid: PyUUID

    class Config:
        from_attributes = True


# Остальные справочники используют ReferenceBase
class ServiceCreate(ReferenceCreate):
    pass


class ServiceResponse(ReferenceResponse):
    pass


class PaymentTypeCreate(ReferenceCreate):
    pass


class PaymentTypeResponse(ReferenceResponse):
    pass


class BusinessSegmentCreate(ReferenceCreate):
    pass


class BusinessSegmentResponse(ReferenceResponse):
    pass


class EvaluationTypeCreate(ReferenceCreate):
    pass


class EvaluationTypeResponse(ReferenceResponse):
    pass


class CostTypeCreate(ReferenceCreate):
    pass


class CostTypeResponse(ReferenceResponse):
    pass


class RevenueStatusCreate(ReferenceCreate):
    pass


class RevenueStatusResponse(ReferenceResponse):
    pass


class CostStatusCreate(ReferenceCreate):
    pass


class CostStatusResponse(ReferenceResponse):
    pass
