from pydantic import BaseModel, Field


class LimitOffsetImplPaginationParams(BaseModel):
    limit: int = Field(..., ge=1, le=100)
    offset: int = Field(..., ge=0)


class SpyCatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: str
    salary: float = Field(..., ge=0)


class SpyCatDetailBase(SpyCatBase):
    years_of_experience: int = Field(..., ge=0)


class SpyCatCreate(SpyCatDetailBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: float = Field(..., ge=0)


class SpyCatBaseResponse(SpyCatBase):
    id: int


class SpyCatDetailResponse(SpyCatDetailBase):
    id: int


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=100)
    notes: str | None = None
    completed: bool = False


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: str | None = None
    completed: bool | None = None


class TargetResponse(TargetBase):
    id: int


class MissionBase(BaseModel):
    completed: bool = False


class MissionCreate(MissionBase):
    targets: list[TargetCreate]


class MissionAssign(BaseModel):
    cat_id: int


class MissionResponse(MissionBase):
    id: int
    cat_id: int | None = None
    targets: list[TargetResponse]


class PaginatedResponse[T](BaseModel):
    results: list[T]
    count: int
    next_url: str | None = None
