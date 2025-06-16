from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class CatchEventBase(BaseModel):
    """Base catch event schema"""

    set_id: int = Field(..., description="ID of the set this catch belongs to")
    timestamp: datetime = Field(..., description="When the catch occurred")
    player_id: int = Field(..., description="ID of the player who made the catch")
    location_x: Optional[float] = Field(None, description="X coordinate of the catch")
    location_y: Optional[float] = Field(None, description="Y coordinate of the catch")
    throw_event_id: int = Field(
        ..., description="ID of the throw event that was caught"
    )
    rebound_catch: bool = Field(False, description="Whether this was a rebound catch")


# Requests
class CatchEventCreate(CatchEventBase):
    """Schema for creating new catch events"""

    pass


class CatchEventUpdate(BaseModel):
    """Schema for updating catch events"""

    set_id: Optional[int] = Field(
        None, description="ID of the set this catch belongs to"
    )
    timestamp: Optional[datetime] = Field(None, description="When the catch occurred")
    player_id: Optional[int] = Field(
        None, description="ID of the player who made the catch"
    )
    location_x: Optional[float] = Field(None, description="X coordinate of the catch")
    location_y: Optional[float] = Field(None, description="Y coordinate of the catch")
    throw_event_id: Optional[int] = Field(
        None, description="ID of the throw event that was caught"
    )
    rebound_catch: Optional[bool] = Field(
        None, description="Whether this was a rebound catch"
    )


# Responses
class CatchEventResponse(CatchEventBase):
    """Standard catch event response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
