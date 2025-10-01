from pydantic import BaseModel, Field


class TargetBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=100)
    notes: str | None = None
    completed: bool = False


class TargetCreateSchema(TargetBaseSchema):
    pass


class TargetUpdateSchema(BaseModel):
    notes: str | None = None
    completed: bool | None = None


class TargetResponseSchema(TargetBaseSchema):
    id: int
