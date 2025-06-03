from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import BaseModel

if TYPE_CHECKING:
    from models.set_event import SetEvent
# Target location data can be calculated from the movement tracking

class ThrowEvent(BaseModel):
    """ A throw in a set of dodgeball """
    
    __tablename__ = "throw_events"
    
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    target_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"))
    outcome: Mapped[str]
    valid_attempt: Mapped[bool] = mapped_column(default=True)
    
    set_event: Mapped["SetEvent"] = relationship(back_populates="throw_events")