from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request

from src.dependencies.pagination import limit_offset_pagination_dependency
from src.errors.base import NotFoundError
from src.errors.missions import AssignedMissionCannotBeDeletedError, CatAlreadyHasActiveMissionError
from src.schemas.base import PaginatedResponseSchema
from src.schemas.missions import MissionAssignSchema, MissionCreate, MissionDetailResponseSchema, MissionResponseSchema
from src.services.missions import MissionService
from src.structures import LimitOffsetImplPaginationParams
from src.utils.pagination import build_next_url


router = APIRouter(prefix='/missions', tags=['Missions'])


@router.post('', response_model=MissionDetailResponseSchema, status_code=HTTPStatus.CREATED)
async def create_mission(mission: MissionCreate, mission_service: Annotated[MissionService, Depends()]):
    """
    Create a mission with targets (1–3 targets).
    """
    return await mission_service.create(mission)


@router.get('', response_model=PaginatedResponseSchema[MissionResponseSchema])
async def get_missions_list(
    request: Request,
    mission_service: Annotated[MissionService, Depends()],
    pagination_params: Annotated[LimitOffsetImplPaginationParams, Depends(limit_offset_pagination_dependency)],
):
    """List all missions with their targets."""
    missions, count = await mission_service.get_paginated(pagination_params=pagination_params)
    return PaginatedResponseSchema[MissionResponseSchema](
        results=missions,
        next_url=build_next_url(pagination_params=pagination_params, request=request, total_count=count),
    )


@router.get('/{mission_id}', response_model=MissionDetailResponseSchema)
async def get_mission(mission_id: int, mission_service: Annotated[MissionService, Depends()]):
    try:
        return await mission_service.get_by_id(mission_id=mission_id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Mission not found',
        ) from err


@router.delete('/{mission_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_mission(mission_id: int, mission_service: Annotated[MissionService, Depends()]):
    try:
        await mission_service.delete(mission_id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Mission not found',
        ) from err
    except AssignedMissionCannotBeDeletedError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Assigned mission cannot be deleted',
        ) from err

@router.patch('/{mission_id}/assign', response_model=MissionResponseSchema)
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
    except CatAlreadyHasActiveMissionError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(err),
        ) from err
