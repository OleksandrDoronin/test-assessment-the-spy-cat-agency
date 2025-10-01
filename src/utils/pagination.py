from fastapi import Request

from src.structures import LimitOffsetImplPaginationParams


def build_next_url(
    pagination_params: LimitOffsetImplPaginationParams, request: Request, total_count: int
) -> str | None:
    if pagination_params.offset + pagination_params.limit >= total_count:
        return None
    return str(
        request.url.replace_query_params(
            offset=pagination_params.offset + pagination_params.limit,
            limit=pagination_params.limit,
        )
    )
