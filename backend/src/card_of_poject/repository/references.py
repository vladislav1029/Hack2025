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
    async def get_by_name(self, name: str) -> Stage | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class ServiceRepository(BaseRepository[Service]):
    async def get_by_name(self, name: str) -> Service | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class PaymentTypeRepository(BaseRepository[PaymentType]):
    async def get_by_name(self, name: str) -> PaymentType | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class BusinessSegmentRepository(BaseRepository[BusinessSegment]):
    async def get_by_name(self, name: str) -> BusinessSegment | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class EvaluationTypeRepository(BaseRepository[EvaluationType]):
    async def get_by_name(self, name: str) -> EvaluationType | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class CostTypeRepository(BaseRepository[CostType]):
    async def get_by_name(self, name: str) -> CostType | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class RevenueStatusRepository(BaseRepository[RevenueStatus]):
    async def get_by_name(self, name: str) -> RevenueStatus | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()


class CostStatusRepository(BaseRepository[CostStatus]):
    async def get_by_name(self, name: str) -> CostStatus | None:
        qwery = select(self.model).where(self.model.name == name)
        result = await self.session.execute(qwery)
        return result.scalars().first()

class CommentRepository(BaseRepository[Comment]):
    async def list_for_project(self, project_id: IDType) -> List[Comment]:
        query = (
            select(Comment)
            .where(Comment.project_id == project_id)
            .options(selectinload(Comment.author))
        )
        result = await self.session.execute(query)
        return result.scalars().all()
