from typing import Annotated

from fastapi import Depends

from src.errors.cats import CatNotFoundError
from src.models import SpyCat
from src.repositories.cats import CatSpyRepository
from src.schemas.cats import (
    SpyCatCreateSchema,
    SpyCatDetailResponseSchema,
    SpyCatListResponseSchema,
    SpyCatUpdateSchema,
)
from src.structures import LimitOffsetImplPaginationParams


class CatSpyService:
    def __init__(self, cat_spy_repository: Annotated[CatSpyRepository, Depends()]):
        self._cat_spy_repository = cat_spy_repository

    async def create(self, cat: SpyCatCreateSchema) -> SpyCatDetailResponseSchema:
        cat_to_create = SpyCat(
            name=cat.name,
            breed=cat.breed,
            years_of_experience=cat.years_of_experience,
            salary=cat.salary,
        )
        cat = await self._cat_spy_repository.create(cat_to_create)
        return SpyCatDetailResponseSchema(
            id=cat.id,
            name=cat.name,
            breed=cat.breed,
            years_of_experience=cat.years_of_experience,
            salary=cat.salary,
        )

    async def get_paginated(
        self, pagination_params: LimitOffsetImplPaginationParams
    ) -> tuple[list[SpyCatListResponseSchema], int]:
        count = await self._cat_spy_repository.get_count()
        if not count:
            return [], 0
        cats = await self._cat_spy_repository.get_paginated(pagination_params=pagination_params)
        return [
            SpyCatListResponseSchema(
                id=cat.id,
                name=cat.name,
                breed=cat.breed,
                salary=cat.salary,
            )
            for cat in cats
        ], count

    async def get_by_id(self, cat_id: int) -> SpyCatDetailResponseSchema:
        cat = await self._cat_spy_repository.get_by_id(cat_id)
        if cat is None:
            raise CatNotFoundError
        return SpyCatDetailResponseSchema(
            id=cat.id,
            name=cat.name,
            breed=cat.breed,
            years_of_experience=cat.years_of_experience,
            salary=cat.salary,
        )

    async def update(self, cat_id: int, cat_to_update: SpyCatUpdateSchema) -> SpyCatDetailResponseSchema:
        cat = await self._cat_spy_repository.get_by_id(cat_id)
        if cat is None:
            raise CatNotFoundError
        cat.salary = cat_to_update.salary
        cat = await self._cat_spy_repository.update(entity=cat)
        return SpyCatDetailResponseSchema(
            id=cat.id,
            name=cat.name,
            breed=cat.breed,
            years_of_experience=cat.years_of_experience,
            salary=cat.salary,
        )

    async def delete(self, cat_id: int):
        is_deleted = await self._cat_spy_repository.delete(cat_id)
        if not is_deleted:
            raise CatNotFoundError
