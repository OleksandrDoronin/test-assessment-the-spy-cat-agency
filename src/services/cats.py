import itertools
from typing import TYPE_CHECKING, Annotated

from async_lru import alru_cache
from fastapi import Depends

from src.errors.cats import CatNotFoundError, InvalidBreedError
from src.models import SpyCat
from src.repositories.rest_api.breads_api import TheCatApiRepository
from src.repositories.sql_repos.cats import CatSpyRepository
from src.schemas.cats import (
    SpyCatCreateSchema,
    SpyCatDetailResponseSchema,
    SpyCatListResponseSchema,
    SpyCatUpdateSchema,
)
from src.structures import LimitOffsetImplPaginationParams


if TYPE_CHECKING:
    from src.repositories.rest_api.structures import CatBreed


class CatSpyService:
    def __init__(
        self,
        cat_spy_repository: Annotated[CatSpyRepository, Depends()],
        the_cat_api_repository: Annotated[TheCatApiRepository, Depends()],
    ):
        self._cat_spy_repository = cat_spy_repository
        self._the_cat_api_repository = the_cat_api_repository

    async def create(self, cat: SpyCatCreateSchema) -> SpyCatDetailResponseSchema:
        allowed_cat_breeds = await self.get_unique_breeds_names()
        allowed_alternative_breeds = await self.get_unique_alternative_breed_names()
        if cat.breed not in allowed_cat_breeds | allowed_alternative_breeds:
            raise InvalidBreedError

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

    async def get_breeds(self) -> list['CatBreed']:
        return await self._the_cat_api_repository.get_all_breds()

    @alru_cache(maxsize=1, ttl=3600)
    async def get_unique_breeds_names(self) -> set[str]:
        breeds = await self.get_breeds()
        return {breed.name for breed in breeds}

    @alru_cache(maxsize=1, ttl=3600)
    async def get_unique_alternative_breed_names(self) -> set[str]:
        breeds = await self.get_breeds()
        return set(itertools.chain.from_iterable(breed.alt_names for breed in breeds))
