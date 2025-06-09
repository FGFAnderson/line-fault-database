from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import BaseModel

if TYPE_CHECKING:
    from player import Player
    from set import Set
    from throw_event import ThrowEvent


class CatchEvent(BaseModel):
    """ " A catch in a set of dodgeball"""

    __tablename__ = "catch_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    timestamp: Mapped[datetime]
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    location_x: Mapped[Optional[float]]
    location_y: Mapped[Optional[float]]

    throw_event_id: Mapped[int] = mapped_column(ForeignKey("throw_events.id"))
    rebound_catch: Mapped[bool] = mapped_column(default=False)

    throw_event: Mapped["ThrowEvent"] = relationship()
    catcher: Mapped["Player"] = relationship(foreign_keys=[player_id])
    set: Mapped["Set"] = relationship()

    def __repr__(self) -> str:
        return f"<CatchEvent(id={self.id}, catcher={self.player_id})>"
