from pydantic import BaseModel, conlist

from src.schemas.targets import TargetCreateSchema, TargetResponseSchema


class MissionBaseSchema(BaseModel):
    completed: bool = False


class MissionCreate(MissionBaseSchema):
    targets: conlist(item_type=TargetCreateSchema, min_length=1, max_length=3)


class MissionResponseSchema(MissionBaseSchema):
    id: int
    cat_id: int | None = None


class MissionDetailResponseSchema(MissionResponseSchema):
    targets: list[TargetResponseSchema]


class MissionAssignSchema(BaseModel):
    cat_id: int
