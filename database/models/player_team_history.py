from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import BaseModel

if TYPE_CHECKING:
    from .player import Player


class PlayerTeamHistory(BaseModel):
    __tablename__ = "player_team_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    joined_at: Mapped[datetime]
    left_at: Mapped[Optional[datetime]]

    player: Mapped["Player"] = relationship(back_populates="team_history")
