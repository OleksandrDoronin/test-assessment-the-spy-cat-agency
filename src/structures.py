from pydantic import BaseModel, Field


class LimitOffsetImplPaginationParams(BaseModel):
    limit: int = Field(..., ge=1, le=100)
    offset: int = Field(..., ge=0)
