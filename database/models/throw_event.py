from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import BaseModel

if TYPE_CHECKING:
    from .set import Set


class ThrowEvent(BaseModel):
    """A throw in a set of dodgeball"""

    __tablename__ = "throw_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    timestamp: Mapped[datetime]
    target_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"))
    location_x: Mapped[Optional[float]]
    location_y: Mapped[Optional[float]]
    target_location_x: Mapped[Optional[float]]
    target_location_y: Mapped[Optional[float]]
    valid_attempt: Mapped[bool] = mapped_column(default=True)
    target_had_ball: Mapped[bool] = mapped_column(default=False)
    was_blocked: Mapped[bool] = mapped_column(default=True)

    set: Mapped["Set"] = relationship()
