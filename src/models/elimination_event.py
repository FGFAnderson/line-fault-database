from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import BaseModel

class EliminationCause(str, Enum):
    DIRECT_HIT = "direct_hit"
    DEFLECTION_HIT = "deflection_hit"
    THROW_CAUGHT = "throw_caught"
    LINE_FAULT = "line_fault"
    INVALID_ATTEMPT = "invalid_attempt"
    PENALTY = "penalty"
    LOSS_OF_CONTROL = "loss_of_control" 

if TYPE_CHECKING:
    from models.player import Player
    from models.throw_event import ThrowEvent
    from models.catch_event import CatchEvent
    from models.set import Set

class Elimination(BaseModel):
    """ An elimination be caused by a throw, catch or other found in the EliminationCause enum """
    
    __tablename__ = "eliminations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    eliminated_player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    cause: Mapped[EliminationCause]
    throw_event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("throw_events.event_id"))
    catch_event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("catch_events.event_id"))
    elimination_location_x: Mapped[Optional[float]]
    elimination_location_y: Mapped[Optional[float]]
    
    eliminated_player: Mapped["Player"] = relationship()
    throw_event: Mapped[Optional["ThrowEvent"]] = relationship(back_populates="eliminations")
    catch_event: Mapped[Optional["CatchEvent"]] = relationship(back_populates="eliminations")
    set: Mapped["Set"] = relationship()
    
    def __repr__(self) -> str:
        return f"<Elimination(id={self.id}, player={self.eliminated_player_id}, cause={self.cause})>"