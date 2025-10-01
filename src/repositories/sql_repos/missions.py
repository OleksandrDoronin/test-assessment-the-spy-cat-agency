from sqlalchemy import select, and_

from src.models import Mission
from src.repositories.sql_repos.base import BaseRepository


class MissionRepository(BaseRepository[Mission]):
    model = Mission

    async def get_active_missions_by_cat_id(self, cat_id: int) -> list[Mission]:
        stmt = select(self.model).where(and_(self.model.cat_id == cat_id, self.model.completed == False))
        result = await self._session.execute(stmt)
        return result.all()
