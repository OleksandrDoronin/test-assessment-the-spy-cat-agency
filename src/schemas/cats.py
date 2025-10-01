from pydantic import BaseModel, Field


class SpyCatBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: str
    salary: float = Field(..., ge=0)


class SpyCatDetailBaseSchema(SpyCatBaseSchema):
    years_of_experience: int = Field(..., ge=0)


class SpyCatCreateSchema(SpyCatDetailBaseSchema):
    pass


class SpyCatUpdateSchema(BaseModel):
    salary: float = Field(..., ge=0)


class SpyCatListResponseSchema(SpyCatBaseSchema):
    id: int


class SpyCatDetailResponseSchema(SpyCatListResponseSchema):
    id: int
    years_of_experience: int


class PaginatedResponseSchema[T](BaseModel):
    results: list[T]
    next_url: str | None = None
