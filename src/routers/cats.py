from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request

from src.dependencies.pagination import limit_offset_pagination_dependency
from src.errors.base import NotFoundError
from src.schemas.cats import (
    PaginatedResponseSchema,
    SpyCatCreateSchema,
    SpyCatDetailResponseSchema,
    SpyCatListResponseSchema,
    SpyCatUpdateSchema,
)
from src.services.cats import CatSpyService
from src.structures import LimitOffsetImplPaginationParams
from src.utils.pagination import build_next_url


router = APIRouter(prefix='/cats', tags=['Cats'])


@router.post('', response_model=SpyCatDetailResponseSchema, status_code=HTTPStatus.OK)
async def create_cat(cat: SpyCatCreateSchema, cat_spy_service: Annotated[CatSpyService, Depends()]):
    return await cat_spy_service.create(cat)


@router.get('', response_model=PaginatedResponseSchema[SpyCatListResponseSchema])
async def get_cats_list(
    request: Request,
    pagination_params: Annotated[LimitOffsetImplPaginationParams, Depends(limit_offset_pagination_dependency)],
    cat_spy_service: Annotated[CatSpyService, Depends()],
):
    cats, count = await cat_spy_service.get_paginated(pagination_params=pagination_params)
    return PaginatedResponseSchema[SpyCatListResponseSchema](
        results=cats,
        next_url=build_next_url(
            pagination_params=pagination_params,
            request=request,
            total_count=count,
        ),
    )


@router.get('/{cat_id}', response_model=SpyCatDetailResponseSchema)
async def get_cat(cat_id: int, cat_spy_service: Annotated[CatSpyService, Depends()]):
    try:
        return await cat_spy_service.get_by_id(cat_id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Cat not found',
        ) from err


@router.patch('/{cat_id}', response_model=SpyCatDetailResponseSchema)
async def update_cat(cat_id: int, spy_cat: SpyCatUpdateSchema, cat_spy_service: Annotated[CatSpyService, Depends()]):
    try:
        return await cat_spy_service.update(cat_id, spy_cat)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Cat not found',
        ) from err


@router.delete('/{cat_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_cat(cat_id: int, cat_spy_service: Annotated[CatSpyService, Depends()]):
    try:
        await cat_spy_service.delete(cat_id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Cat not found',
        ) from err
