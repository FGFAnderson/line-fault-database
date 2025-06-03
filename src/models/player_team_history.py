from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from models.base import BaseModel


class PlayerTeamHistory(BaseModel):
    __tablename__ = "player_team_history"
    

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime())
    left_at = Mapped[datetime] = mapped_column()

    user = relationship("User", back_populates="team_memberships")
    team = relationship("Team", back_populates="user_memberships")