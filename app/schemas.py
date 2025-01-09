from pydantic import BaseModel, field_validator
from typing import List, Optional


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class SpyCatCreate(SpyCatBase):
    pass


class SpyCat(SpyCatBase):
    id: int

    class Config:
        orm_mode = True


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    complete: bool = False


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    complete: bool = False

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("country")
    def country_not_empty(cls, v):
        if not v:
            raise ValueError("Country cannot be empty")
        return v

    @field_validator("complete")
    def status_valid(cls, v):
        if v not in [True, False]:
            raise ValueError("Status must be either True or False")
        return v


class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    complete: Optional[bool] = None

    class Config:
        orm_mode = True


class MissionBase(BaseModel):
    complete: bool = False


class MissionCreate(BaseModel):
    targets: List[TargetCreate]

    @field_validator('targets')
    def validate_targets_count(cls, v):
        if len(v) < 1 or len(v) > 3:
            raise ValueError("The number of targets must be between 1 and 3.")
        return v


class Mission(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[Target]

    class Config:
        orm_mode = True

