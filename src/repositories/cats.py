from src.models import SpyCat
from src.repositories.base import BaseRepository


class CatSpyRepository(BaseRepository[SpyCat]):
    model = SpyCat
