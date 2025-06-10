from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    """Base team schema"""

    name: str = Field(..., min_length=1, max_length=120, description="Team name")
    logo_url: Optional[str] = Field(None, description="Team logo image URL")


# Requests
class TeamCreate(TeamBase):
    """Schema for creating new teams"""

    pass


class TeamUpdate(BaseModel):
    """Schema for updating teams"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=120, description="Team name"
    )
    logo_url: Optional[str] = Field(None, description="Team logo image URL")


# Responses
class TeamResponse(TeamBase):
    """Standard team response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
