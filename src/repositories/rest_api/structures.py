from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator, Field


class Weight(BaseModel):
    imperial: str
    metric: str


class CatBreed(BaseModel):
    weight: Weight
    id: str
    name: str
    cfa_url: Optional[str] = None
    vetstreet_url: Optional[str] = None
    vcahospitals_url: Optional[str] = None
    temperament: str | None = None
    origin: str | None = None
    country_codes: str | None = None
    country_code: str | None = None
    description: str | None = None
    life_span: str | None = None
    indoor: int | None = None
    lap: Optional[int] = None
    alt_names: list[str] = Field(default_factory=list)
    adaptability: int | None = None
    affection_level: int | None = None
    child_friendly: int | None = None
    dog_friendly: int | None = None
    energy_level: int | None = None
    grooming: int | None = None
    health_issues: int | None = None
    intelligence: int | None = None
    shedding_level: int | None = None
    social_needs: int | None = None
    stranger_friendly: int | None = None
    vocalisation: int | None = None
    experimental: int | None = None
    hairless: int | None = None
    natural: int | None = None
    rare: int | None = None
    rex: int | None = None
    suppressed_tail: int | None = None
    short_legs: int | None = None
    wikipedia_url: Optional[HttpUrl] = None
    hypoallergenic: int | None = None
    reference_image_id: str | None = None

    @field_validator('alt_names', mode='before')
    def parse_alt_names(cls, alt_names: str) -> list[str]:
        if alt_names:
            return [name.strip() for name in alt_names.split(',')]
        return []
