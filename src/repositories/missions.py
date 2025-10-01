from src.models import Mission
from src.repositories.base import BaseRepository


class MissionRepository(BaseRepository[Mission]):
    model = Mission
