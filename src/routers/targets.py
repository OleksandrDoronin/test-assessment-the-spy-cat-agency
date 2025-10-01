from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.errors.base import NotFoundError
from src.errors.missions import CannotUpdateCompletedMissionError
from src.errors.targets import CannotUpdateCompletedTargetError
from src.schemas.targets import TargetResponseSchema, TargetUpdateSchema
from src.services.targets import TargetService


router = APIRouter(tags=['Targets'])


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
    except (CannotUpdateCompletedMissionError, CannotUpdateCompletedTargetError) as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(err),
        )
