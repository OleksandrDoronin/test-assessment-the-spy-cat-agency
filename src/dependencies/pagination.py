from fastapi import Query

from src.structures import LimitOffsetImplPaginationParams


def limit_offset_pagination_dependency(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> LimitOffsetImplPaginationParams:
    return LimitOffsetImplPaginationParams(
        limit=limit,
        offset=offset,
    )
