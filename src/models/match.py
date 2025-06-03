from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from models.base import BaseModel

if TYPE_CHECKING:
    from models.competition import Competition
class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Match(BaseModel):
    """ A match in a league or competion """
    
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    competition: Mapped["Competition"] = relationship(back_populates="matches")
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    team1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    match_date: Mapped[datetime]
    status: Mapped["MatchStatus"] = mapped_column(SQLEnum(MatchStatus))

    def __repr__(self) -> str:
        return f"<Match(id={self.id}, team1_id={self.team1_id}, team2_id={self.team2_id}, status='{self.status}')>"