# INFO: No protocol because overkill for MVP
from abc import ABC, abstractmethod
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID as PyUUID

from src.core.auth.models import User
from src.models import Base

Entity = TypeVar("Entity", bound=Base)
IDType = Union[int, PyUUID]


class AbstractRepository(ABC, Generic[Entity]):
    model: Type[Entity]

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    @abstractmethod
    async def add(self):
        raise NotImplemented

    @abstractmethod
    async def get(self):
        raise NotImplemented

    @abstractmethod
    async def list(
        self,
        offset: int = 0,
        limit: int = 20,
        order_by: Optional[str] = None,
    ) -> List[Entity]:

        raise NotImplemented

    @abstractmethod
    async def delete(self):
        raise NotImplemented


class CRUDRepository(AbstractRepository[Entity]):
    """Базовый репозиторий с CRUD для всех сущностей"""

    async def add(self, instance: Entity) -> Entity:
        self.session.add(instance)
        await self.session.commit()  # Чтобы получить ID сразу
        await self.session.refresh(instance)
        return instance

    async def get(self, oid: IDType) -> Optional[Entity]:
        return await self.session.get(self.model, oid)

    async def list(
        self,
        offset: int = 0,
        limit: int = 20,
        order_by: Optional[str] = None,
    ) -> List[Entity]:
        stmt = select(self.model)
        if order_by:
            order_column = getattr(self.model, order_by, None)
            if order_column is not None:
                stmt = stmt.order_by(order_column)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, oid: IDType, data: Dict[str, Any]) -> Optional[Entity]:
        stmt = (
            update(self.model)
            .where(self.model.oid == oid)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, oid: IDType) -> Optional[Entity]:
        instance = await self.get(oid)
        if not instance:
            return None
        await self.session.delete(instance)
        await self.session.commit()
        return instance


class UserRepository(AbstractRepository[User]):
    model = User

    async def add(self, model: User) -> User:

        self.session.add(model)
        await self.session.commit()
        # Если элемент получает значение при коммите в БД

        # однако чтоит также использовать при асинхронном взаимодействие (для возврата объект) иначе маппить
        # await self.session.refresh(instance=model)
        return model

    async def get(self, oid: IDType):
        return await self.session.get(self.model, oid)

    async def get_by_email(self, email: str) -> User | None:  # валидируется до этого
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        offset: int = 0,
        limit: int = 5,
        order_by=None,
    ) -> List[User]:  # стоит передовать параметры через класс пагинации
        results = await self.session.execute(
            select(self.model).offset(offset=offset).limit(limit=limit)
        )
        return results.scalars().all()

    async def delete(self, oid: IDType):
        instance = await self.get(oid)
        if not instance:
            return None
        self.session.delete(instance=instance)
        await self.session.commit()
        return instance
