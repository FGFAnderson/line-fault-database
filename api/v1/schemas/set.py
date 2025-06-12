from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class SetBase(BaseModel):
    """Base set schema"""

    match_id: int = Field(..., description="ID of the match this set belongs to")
    set_number: int = Field(..., ge=1, description="Set number within the match")
    start_time: datetime = Field(..., description="When the set started")
    end_time: Optional[datetime] = Field(None, description="When the set ended")
    winning_team_id: Optional[int] = Field(None, description="ID of the winning team")


# Requests
class SetCreate(SetBase):
    """Schema for creating new sets"""

    pass


class SetUpdate(BaseModel):
    """Schema for updating sets"""

    match_id: Optional[int] = Field(
        None, description="ID of the match this set belongs to"
    )
    set_number: Optional[int] = Field(
        None, ge=1, description="Set number within the match"
    )
    start_time: Optional[datetime] = Field(None, description="When the set started")
    end_time: Optional[datetime] = Field(None, description="When the set ended")
    winning_team_id: Optional[int] = Field(None, description="ID of the winning team")


# Responses
class SetResponse(SetBase):
    """Standard set response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
