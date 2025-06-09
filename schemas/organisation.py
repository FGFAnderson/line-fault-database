from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

from database.enums.country_codes import CountryCode


class OrganisationBase(BaseModel):
    """Base organisation schema"""

    name: str = Field(
        ..., min_length=1, max_length=120, description="Organisation name"
    )
    country_code: CountryCode = Field(
        ...,
        description="Extended ISO country code's with ENG, SCO, WAL, NIR, IRL and WLD (For world)",
    )
    region: Optional[str] = Field(None, max_length=100, description="Geographic region")
    website: Optional[HttpUrl] = Field(None, description="Organisation website")
    logo_url: Optional[HttpUrl] = Field(None, description="Logo image URL")


class OrganisationResponse(OrganisationBase):
    """Standard organisation response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
