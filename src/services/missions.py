from typing import Annotated

from fastapi import Depends

from src.errors.cats import CatNotFoundError
from src.errors.missions import MissionNotFoundError
from src.models.missions import Mission
from src.models.targets import Target
from src.repositories.cats import CatSpyRepository
from src.repositories.missions import MissionRepository
from src.repositories.targets import TargetRepository
from src.schemas.missions import MissionCreate, MissionAssignSchema, MissionResponseSchema
from src.schemas.targets import TargetResponseSchema
from src.structures import LimitOffsetImplPaginationParams


class MissionService:
    def __init__(
        self,
        cat_repository: Annotated[CatSpyRepository, Depends()],
        mission_repository: Annotated[MissionRepository, Depends()],
        target_repository: Annotated[TargetRepository, Depends()],
    ):
        self._cat_repository = cat_repository
        self._mission_repository = mission_repository
        self._target_repository = target_repository

    async def create(self, mission: MissionCreate) -> MissionResponseSchema:
        mission_to_create = Mission(completed=mission.completed)
        created_mission = await self._mission_repository.create(mission_to_create)
        targets_to_create = [
            Target(
                name=target.name,
                country=target.country,
                notes=target.notes,
                completed=target.completed,
                mission_id=created_mission.id,
            )
            for target in mission.targets
        ]
        targets = await self._target_repository.bulk_create(entities=targets_to_create)

        return MissionResponseSchema(
            id=created_mission.id,
            completed=created_mission.completed,
            cat_id=created_mission.cat_id,
            targets=[
                TargetResponseSchema(
                    id=target.id,
                    name=target.name,
                    country=target.country,
                    notes=target.notes,
                    completed=target.completed,
                )
                for target in targets
            ],
        )

    async def get_paginated(
        self, pagination_params: LimitOffsetImplPaginationParams
    ) -> tuple[list[MissionResponseSchema], int]:
        count = await self._mission_repository.get_count()
        if not count:
            return [], 0
        missions = await self._mission_repository.get_paginated(pagination_params=pagination_params)
        return [
            MissionResponseSchema(
                id=mission.id,
                completed=mission.completed,
                cat_id=mission.cat_id,
                targets=[
                    TargetResponseSchema(
                        id=target.id,
                        name=target.name,
                        country=target.country,
                        notes=target.notes,
                        completed=target.completed,
                    )
                    for target in mission.targets
                ],
            )
            for mission in missions
        ], count

    async def get_by_id(self, mission_id: int) -> MissionResponseSchema:
        mission = await self._mission_repository.get_by_id(mission_id)
        if mission is None:
            raise MissionNotFoundError

        return MissionResponseSchema(
            id=mission.id,
            completed=mission.completed,
            cat_id=mission.cat_id,
            targets=[
                TargetResponseSchema(
                    id=target.id,
                    name=target.name,
                    country=target.country,
                    notes=target.notes,
                    completed=target.completed,
                )
                for target in mission.targets
            ],
        )

    async def assign_cat(self, mission_id: int, mission_to_update: MissionAssignSchema) -> MissionResponseSchema:
        cat = await self._cat_repository.get_by_id(mission_to_update.cat_id)
        if cat is None:
            raise CatNotFoundError

        mission = await self._mission_repository.get_by_id(mission_id)
        if mission is None:
            raise MissionNotFoundError

        mission.cat_id = mission_to_update.cat_id
        updated_mission = await self._mission_repository.update(entity=mission)
        targets = await self._target_repository.get_by_mission_id(mission_id=mission_id)
        return MissionResponseSchema(
            id=updated_mission.id,
            completed=updated_mission.completed,
            cat_id=updated_mission.cat_id,
            targets=[
                TargetResponseSchema(
                    id=target.id,
                    name=target.name,
                    country=target.country,
                    notes=target.notes,
                    completed=target.completed,
                )
                for target in targets
            ],
        )

    async def delete(self, mission_id: int) -> None:
        await self._mission_repository.delete(mission_id)
