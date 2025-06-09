from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from database.models.competition import CompetitionFormat, AgeCategory, CourtSize


class CompetitionBase(BaseModel):
    """Base competition schema"""

    name: str = Field(..., min_length=1, max_length=120, description="Competition name")
    competition_format: CompetitionFormat = Field(
        ..., description="Competition format (league or tournament)"
    )
    organisation_id: int = Field(
        ..., description="ID of the organising organisation", gt=0
    )
    age_category: AgeCategory = Field(
        ..., description="Age category for the competition"
    )
    court_size: CourtSize = Field(..., description="Court size used in the competition")


# Requests
class CompetitionCreate(CompetitionBase):
    """Schema for creating new competitions"""

    pass


class CompetitionUpdate(BaseModel):
    """Schema for updating competitions - all fields optional"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=120, description="Competition name"
    )
    competition_format: Optional[CompetitionFormat] = Field(
        None, description="Competition format (league or tournament)"
    )
    organisation_id: Optional[int] = Field(
        None, description="ID of the organising organisation", gt=0
    )
    age_category: Optional[AgeCategory] = Field(
        None, description="Age category for the competition"
    )
    court_size: Optional[CourtSize] = Field(
        None, description="Court size used in the competition"
    )


# Responses
class CompetitionResponse(CompetitionBase):
    """Standard competition response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
