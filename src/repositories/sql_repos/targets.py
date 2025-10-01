from sqlalchemy import select

from src.models import Target
from src.repositories.sql_repos.base import BaseRepository


class TargetRepository(BaseRepository[Target]):
    model = Target

    async def get_by_mission_id(self, mission_id: int) -> list[Target]:
        stmt = select(self.model).where(self.model.mission_id == mission_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
