from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class ThrowEventBase(BaseModel):
    """Base throw event schema"""

    set_id: int = Field(..., description="ID of the set this throw belongs to")
    player_id: int = Field(..., description="ID of the player who made the throw")
    timestamp: datetime = Field(..., description="When the throw occurred")
    target_player_id: Optional[int] = Field(
        None, description="ID of the targeted player"
    )
    location_x: Optional[float] = Field(
        None, description="X coordinate of the throw origin"
    )
    location_y: Optional[float] = Field(
        None, description="Y coordinate of the throw origin"
    )
    target_location_x: Optional[float] = Field(
        None, description="X coordinate of the throw target"
    )
    target_location_y: Optional[float] = Field(
        None, description="Y coordinate of the throw target"
    )
    valid_attempt: bool = Field(
        True, description="Whether the throw was a valid attempt"
    )
    target_had_ball: bool = Field(
        False, description="Whether the target had a ball when thrown at"
    )
    was_blocked: bool = Field(True, description="Whether the throw was blocked")


# Requests
class ThrowEventCreate(ThrowEventBase):
    """Schema for creating new throw events"""

    pass


class ThrowEventUpdate(BaseModel):
    """Schema for updating throw events"""

    set_id: Optional[int] = Field(
        None, description="ID of the set this throw belongs to"
    )
    player_id: Optional[int] = Field(
        None, description="ID of the player who made the throw"
    )
    timestamp: Optional[datetime] = Field(None, description="When the throw occurred")
    target_player_id: Optional[int] = Field(
        None, description="ID of the targeted player"
    )
    location_x: Optional[float] = Field(
        None, description="X coordinate of the throw origin"
    )
    location_y: Optional[float] = Field(
        None, description="Y coordinate of the throw origin"
    )
    target_location_x: Optional[float] = Field(
        None, description="X coordinate of the throw target"
    )
    target_location_y: Optional[float] = Field(
        None, description="Y coordinate of the throw target"
    )
    valid_attempt: Optional[bool] = Field(
        None, description="Whether the throw was a valid attempt"
    )
    target_had_ball: Optional[bool] = Field(
        None, description="Whether the target had a ball when thrown at"
    )
    was_blocked: Optional[bool] = Field(
        None, description="Whether the throw was blocked"
    )


# Responses
class ThrowEventResponse(ThrowEventBase):
    """Standard throw event response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
