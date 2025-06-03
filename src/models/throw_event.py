from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import BaseModel

if TYPE_CHECKING:
    from set import Set

class ThrowEvent(BaseModel):
    """ A throw in a set of dodgeball """

    __tablename__ = "throw_events"

    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    timestamp: Mapped[datetime]
    target_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"))
    location_x: Mapped[Optional[float]]
    location_y: Mapped[Optional[float]]
    target_location_x: Mapped[Optional[float]]
    target_location_y: Mapped[Optional[float]]
    valid_attempt: Mapped[bool] = mapped_column(default=True)
    was_blocked: Mapped[bool] = mapped_column(default=True)
    
    set: Mapped["Set"] = relationship()
