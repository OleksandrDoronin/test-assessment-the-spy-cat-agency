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
from src.schemas.missions import MissionAssignSchema, MissionCreate, MissionResponseSchema
from src.schemas.targets import TargetResponseSchema, TargetUpdateSchema
from src.services.cats import CatSpyService
from src.services.missions import MissionService
from src.services.targets import TargetService
from src.structures import LimitOffsetImplPaginationParams
from src.utils.pagination import build_next_url


router = APIRouter(prefix='/cats')


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
    await cat_spy_service.delete(cat_id)


@router.post('/missions', response_model=MissionResponseSchema, status_code=HTTPStatus.CREATED)
async def create_mission(mission: MissionCreate, mission_service: Annotated[MissionService, Depends()]):
    return await mission_service.create(mission)


@router.get('/missions', response_model=PaginatedResponseSchema[MissionResponseSchema])
async def get_missions_list(
    request: Request,
    mission_service: Annotated[MissionService, Depends()],
    pagination_params: Annotated[LimitOffsetImplPaginationParams, Depends(limit_offset_pagination_dependency)],
):
    missions, count = await mission_service.get_paginated(pagination_params=pagination_params)
    return PaginatedResponseSchema[MissionResponseSchema](
        results=missions,
        next_url=build_next_url(pagination_params=pagination_params, request=request, total_count=count),
    )


@router.get('/missions/{mission_id}', response_model=MissionResponseSchema)
async def get_mission(mission_id: int, mission_service: Annotated[MissionService, Depends()]):
    try:
        return await mission_service.get_by_id(mission_id=mission_id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Mission not found',
        ) from err


@router.delete('/missions/{mission_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_mission(mission_id: int, mission_service: Annotated[MissionService, Depends()]):
    await mission_service.delete(mission_id)


@router.patch('/missions/{mission_id}/assign', response_model=MissionResponseSchema)
async def assign_cat_to_mission(
    mission_id: int,
    mission: MissionAssignSchema,
    mission_service: Annotated[MissionService, Depends()],
):
    try:
        return await mission_service.assign_cat(mission_id=mission_id, mission_to_update=mission)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Cat or mission not found',
        ) from err


@router.patch('/missions/{mission_id}/targets/{target_id}', response_model=TargetResponseSchema)
async def update_target(
    mission_id: int,
    target_id: int,
    target: TargetUpdateSchema,
    target_service: Annotated[TargetService, Depends()],
):
    try:
        return await target_service.update(mission_id=mission_id, target_id=target_id, target_to_update=target)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Target or mission not found',
        ) from err
