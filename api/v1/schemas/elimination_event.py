from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from database.models.elimination_event import EliminationCause


class EliminationEventBase(BaseModel):
    """Base elimination event schema"""

    set_id: int = Field(..., description="ID of the set this elimination belongs to")
    eliminated_player_id: int = Field(..., description="ID of the eliminated player")
    cause: EliminationCause = Field(..., description="Cause of elimination")
    throw_event_id: Optional[int] = Field(
        None, description="ID of the related throw event"
    )
    catch_event_id: Optional[int] = Field(
        None, description="ID of the related catch event"
    )
    elimination_location_x: Optional[float] = Field(
        None, description="X coordinate of elimination"
    )
    elimination_location_y: Optional[float] = Field(
        None, description="Y coordinate of elimination"
    )


# Requests
class EliminationEventCreate(EliminationEventBase):
    """Schema for creating new elimination events"""

    pass


class EliminationEventUpdate(BaseModel):
    """Schema for updating elimination events"""

    set_id: Optional[int] = Field(
        None, description="ID of the set this elimination belongs to"
    )
    eliminated_player_id: Optional[int] = Field(
        None, description="ID of the eliminated player"
    )
    cause: Optional[EliminationCause] = Field(None, description="Cause of elimination")
    throw_event_id: Optional[int] = Field(
        None, description="ID of the related throw event"
    )
    catch_event_id: Optional[int] = Field(
        None, description="ID of the related catch event"
    )
    elimination_location_x: Optional[float] = Field(
        None, description="X coordinate of elimination"
    )
    elimination_location_y: Optional[float] = Field(
        None, description="Y coordinate of elimination"
    )


# Responses
class EliminationEventResponse(EliminationEventBase):
    """Standard elimination event response for API"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
