from typing import Annotated

from fastapi import Depends

from src.errors.missions import MissionNotFoundError, CannotUpdateCompletedMissionError
from src.errors.targets import TargetNotFoundError, CannotUpdateCompletedTargetError
from src.repositories.sql_repos.missions import MissionRepository
from src.repositories.sql_repos.targets import TargetRepository
from src.schemas.targets import TargetResponseSchema, TargetUpdateSchema


class TargetService:
    def __init__(
        self,
        target_repository: Annotated[TargetRepository, Depends()],
        mission_repository: Annotated[MissionRepository, Depends()],
    ):
        self._target_repository = target_repository
        self._mission_repository = mission_repository

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

        if not target or mission_id != target.mission_id:
            raise TargetNotFoundError
        if mission.completed:
            raise CannotUpdateCompletedMissionError
        if target.completed:
            raise CannotUpdateCompletedTargetError

        if target_to_update.notes is not None:
            target.notes = target_to_update.notes
        if target_to_update.completed is not None:
            target.completed = target_to_update.completed

        updated_target = await self._target_repository.update(entity=target)
        all_mission_targets = await self._target_repository.get_by_mission_id(mission_id)
        if all(target.completed for target in all_mission_targets):
            mission.completed = True
            await self._mission_repository.update(entity=mission)

        return TargetResponseSchema(
            id=updated_target.id,
            name=updated_target.name,
            country=updated_target.country,
            notes=updated_target.notes,
            completed=updated_target.completed,
        )
