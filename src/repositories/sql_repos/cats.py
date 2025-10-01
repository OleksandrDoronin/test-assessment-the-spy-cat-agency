from src.models import SpyCat
from src.repositories.sql_repos.base import BaseRepository


class CatSpyRepository(BaseRepository[SpyCat]):
    model = SpyCat
