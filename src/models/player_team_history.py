from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from models.base import BaseModel

if TYPE_CHECKING:
    from models.team import Team
    from models.player import Player

class PlayerTeamHistory(BaseModel):
    __tablename__ = "player_team_history"
    

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime())
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime())

    player: Mapped["Player"] = relationship(back_populates="team_history")
    team: Mapped["Team"] = relationship(back_populates="teams")
