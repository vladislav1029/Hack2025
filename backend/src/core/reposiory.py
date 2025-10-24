# INFO: No protocol because overkill for MVP
from abc import ABC, abstractmethod
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, List, Type, TypeVar, Union
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
    async def list(self):
        raise NotImplemented

    @abstractmethod
    async def delete(self):
        raise NotImplemented


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
        self, offset: int = 0, limit: int = 5
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
