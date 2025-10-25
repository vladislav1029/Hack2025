from datetime import datetime
from typing import Dict, TypeVar, Generic, Union, Type, List, Optional
from uuid import UUID as PyUUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete
from abc import ABC, abstractmethod
from src.card_of_poject.model import (
    Dashboard,
    ProjectPrediction,
    Report,
)
from src.models import Base

Entity = TypeVar("Entity", bound=Base)
IDType = Union[int, PyUUID]


class AbstractRepository(ABC, Generic[Entity]):
    model: Type[Entity]

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    @abstractmethod
    async def add(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    async def get(self, id: IDType) -> Optional[Entity]:
        pass

    @abstractmethod
    async def list(self) -> List[Entity]:
        pass

    @abstractmethod
    async def delete(self, id: IDType) -> None:
        pass


class BaseRepository(AbstractRepository[Entity], Generic[Entity]):
    def __init__(self, session: AsyncSession, model: Type[Entity]) -> None:
        super().__init__(session)
        self.model = model

    async def add(self, entity: Entity) -> Entity:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def get(self, id: IDType) -> Optional[Entity]:
        query = select(self.model).where(self.model.oid == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list(self) -> List[Entity]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, id: IDType) -> None:
        query = delete(self.model).where(self.model.oid == id)
        await self.session.execute(query)
        await self.session.flush()


# -------------------------------------------------------------------


class ReportRepository(BaseRepository[Report]):
    async def list_by_user(self, user_id: IDType) -> List[Report]:
        query = select(Report).where(Report.created_by == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()


class DashboardRepository(BaseRepository[Dashboard]):
    async def list_by_user(self, user_id: IDType) -> List[Dashboard]:
        query = select(Dashboard).where(Dashboard.created_by == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()


class ProjectPredictionRepository(BaseRepository[ProjectPrediction]):
    async def get_latest(self, project_id: IDType) -> Optional[ProjectPrediction]:
        query = (
            select(ProjectPrediction)
            .where(ProjectPrediction.project_id == project_id)
            .order_by(ProjectPrediction.calculated_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
