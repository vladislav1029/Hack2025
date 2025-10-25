from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.card_of_poject.model import (
    BusinessSegment,
    Comment,
    CostStatus,
    CostType,
    EvaluationType,
    PaymentType,
    RevenueStatus,
    Service,
    Stage,
)
from src.card_of_poject.repository.base_repository import BaseRepository, IDType


class StageRepository(BaseRepository[Stage]):
    pass


class ServiceRepository(BaseRepository[Service]):
    pass


class PaymentTypeRepository(BaseRepository[PaymentType]):
    pass


class BusinessSegmentRepository(BaseRepository[BusinessSegment]):
    pass


class EvaluationTypeRepository(BaseRepository[EvaluationType]):
    pass


class CostTypeRepository(BaseRepository[CostType]):
    pass


class RevenueStatusRepository(BaseRepository[RevenueStatus]):
    pass


class CostStatusRepository(BaseRepository[CostStatus]):
    pass


class CommentRepository(BaseRepository[Comment]):
    async def list_for_project(self, project_id: IDType) -> List[Comment]:
        query = (
            select(Comment)
            .where(Comment.project_id == project_id)
            .options(selectinload(Comment.author))
        )
        result = await self.session.execute(query)
        return result.scalars().all()
