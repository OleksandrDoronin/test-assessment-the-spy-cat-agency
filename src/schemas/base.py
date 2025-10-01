from pydantic import BaseModel


class PaginatedResponseSchema[T](BaseModel):
    results: list[T]
    next_url: str | None = None
