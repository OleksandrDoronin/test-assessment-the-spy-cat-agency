from abc import ABCMeta, abstractmethod
from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_db_session
from src.structures import LimitOffsetImplPaginationParams


class BaseRepository[T](metaclass=ABCMeta):
    @property
    @abstractmethod
    def model(self) -> Type[T]:
        raise NotImplementedError

    def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]):
        self._session = session

    async def create(self, entity: T) -> T:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def bulk_create(self, entities: list[T]) -> list[T]:
        self._session.add_all(entities)
        await self._session.commit()
        for entity in entities:
            await self._session.refresh(entity)
        return entities

    async def get_paginated(self, pagination_params: LimitOffsetImplPaginationParams, **filters: dict) -> list[T]:
        stmt = select(self.model).filter_by(**filters).limit(pagination_params.limit).offset(pagination_params.offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def get_by_id(self, entity_id: int) -> T:
        result = await self._session.execute(select(self.model).where(self.model.id == entity_id))
        return result.scalar_one_or_none()

    async def update(self, entity: T) -> T:
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity_id: int) -> bool:
        """
        Delete entity by id.

        Returns True if entity was deleted, False otherwise.
        """
        entity = await self.get_by_id(entity_id)
        if entity:
            await self._session.delete(entity)
            await self._session.commit()
            return True

        return False
