from urllib.parse import urljoin

from async_lru import alru_cache
from fastapi import Depends
from httpx import AsyncClient

from src.dependencies.http import get_http_client
from src.repositories.rest_api.structures import CatBreed


class TheCatApiRepository:
    def __init__(self, client: AsyncClient = Depends(get_http_client)):
        self._client = client
        self._base_url = 'https://api.thecatapi.com'

    def _build_url(self, path: str) -> str:
        return urljoin(self._base_url, path)

    @alru_cache(maxsize=1, ttl=3600)  # cache for 1 hour
    async def get_all_breds(self) -> list[CatBreed]:
        response = await self._client.get(url=self._build_url('v1/breeds'))
        response.raise_for_status()
        response_json = response.json()
        return [CatBreed(**breed) for breed in response_json]
