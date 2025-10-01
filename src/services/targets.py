from typing import Annotated

from fastapi import Depends

from src.errors.missions import MissionNotFoundError
from src.errors.targets import TargetNotFoundError
from src.repositories.missions import MissionRepository
from src.repositories.targets import TargetRepository
from src.schemas.targets import TargetResponseSchema, TargetUpdateSchema


class TargetService:
    def __init__(
        self,
        target_repository: Annotated[TargetRepository, Depends()],
        mission_repository: Annotated[MissionRepository, Depends()],
    ):
        self._target_repository = target_repository
        self._mission_repository = mission_repository

    async def get_by_id(self, target_id: int) -> TargetResponseSchema:
        target = await self._target_repository.get_by_id(target_id)
        if target is None:
            raise TargetNotFoundError
        return TargetResponseSchema(
            id=target.id,
            name=target.name,
            country=target.country,
            notes=target.notes,
            completed=target.completed,
        )

    async def update(
        self,
        mission_id: int,
        target_id: int,
        target_to_update: TargetUpdateSchema,
    ) -> TargetResponseSchema:
        mission = await self._mission_repository.get_by_id(mission_id)
        if mission is None:
            raise MissionNotFoundError

        target = await self._target_repository.get_by_id(target_id)
        if mission_id != target.mission_id:
            raise TargetNotFoundError

        if target_to_update.notes is not None:
            target.notes = target_to_update.notes
        if target_to_update.completed is not None:
            target.completed = target_to_update.completed
        updated_target = await self._target_repository.update(entity=target)
        return TargetResponseSchema(
            id=updated_target.id,
            name=updated_target.name,
            country=updated_target.country,
            notes=updated_target.notes,
            completed=updated_target.completed,
        )

    async def delete(self, target_id: int) -> None:
        await self._target_repository.delete(target_id)
