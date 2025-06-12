from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MatchStatus(str, Enum):
    """Match status enumeration"""

    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MatchBase(BaseModel):
    """Base match schema"""

    competition_id: int = Field(..., description="Competition ID")
    team1_id: int = Field(..., description="First team ID")
    team2_id: int = Field(..., description="Second team ID")
    match_date: datetime = Field(..., description="Match date and time")
    status: MatchStatus = Field(
        default=MatchStatus.SCHEDULED, description="Match status"
    )


# Requests
class MatchCreate(MatchBase):
    """Schema for creating new matches"""

    pass


class MatchUpdate(BaseModel):
    """Schema for updating matches"""

    competition_id: Optional[int] = Field(None, description="Competition ID")
    team1_id: Optional[int] = Field(None, description="First team ID")
    team2_id: Optional[int] = Field(None, description="Second team ID")
    match_date: Optional[datetime] = Field(None, description="Match date and time")
    status: Optional[MatchStatus] = Field(None, description="Match status")


# Responses
class MatchResponse(MatchBase):
    """Standard match response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Optional: Response with related data
class MatchResponseWithTeams(MatchResponse):
    """Extended match response including team information"""

    team1_name: Optional[str] = Field(None, description="First team name")
    team2_name: Optional[str] = Field(None, description="Second team name")
    competition_name: Optional[str] = Field(None, description="Competition name")
