from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import BaseModel

class EliminationCause(str, Enum):
    DIRECT_HIT = "direct_hit"
    DEFLECTION_HIT = "deflection_hit"
    THROW_CAUGHT = "throw_caught"
    LINE_FAULT = "line_fault"
    INVALID_ATTEMPT = "invalid_attempt"
    PENALTY = "penalty"
    LOSS_OF_CONTROL = "loss_of_control" 

if TYPE_CHECKING:
    from .player import Player
    from .set import Set

class EliminationEvent(BaseModel):
    """ An elimination be caused by a throw, catch or other found in the EliminationCause enum """
    
    __tablename__ = "eliminations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    eliminated_player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    cause: Mapped[EliminationCause]
    throw_event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("throw_events.id"))
    catch_event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("catch_events.id"))
    elimination_location_x: Mapped[Optional[float]]
    elimination_location_y: Mapped[Optional[float]]
    
    eliminated_player: Mapped["Player"] = relationship()
    set: Mapped["Set"] = relationship()
    
    def __repr__(self) -> str:
        return f"<Elimination(id={self.id}, player={self.eliminated_player_id}, cause={self.cause})>"