from pydantic import BaseModel

from src.schemas.targets import TargetCreateSchema, TargetResponseSchema


class MissionBaseSchema(BaseModel):
    completed: bool = False


class MissionCreate(MissionBaseSchema):
    targets: list[TargetCreateSchema]


class MissionAssignSchema(BaseModel):
    cat_id: int


class MissionResponseSchema(MissionBaseSchema):
    id: int
    cat_id: int | None = None
    targets: list[TargetResponseSchema]
