

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import BaseModel

if TYPE_CHECKING:
    from set import Set

class MovementEvent(BaseModel):
    """ A movement checked at intervals using object recognition """

    __tablename__ = "movement_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    timestamp: Mapped[datetime]
    start_x: Mapped[float]
    start_y: Mapped[float]
    end_x: Mapped[float]
    end_y: Mapped[float]
    
    set: Mapped["Set"] = relationship()
