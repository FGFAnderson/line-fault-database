from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Index, SmallInteger, func
from models.base import Base
class TeamCompetition(Base):
    """Junction table for teams participating in competitions"""
    __tablename__ = "team_competitions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"), nullable=False)
    joined_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    points: Mapped[int] = mapped_column(SmallInteger, default=0)
    wins: Mapped[int] = mapped_column(SmallInteger, default=0)
    losses: Mapped[int] = mapped_column(SmallInteger, default=0)
    draws: Mapped[int] = mapped_column(SmallInteger, default=0)
    team: Mapped["Team"] = relationship(back_populates="team_competitions")
    competition: Mapped["Competition"] = relationship(back_populates="team_competitions")
    
    __table_args__ = (
        Index('ix_team_competition_unique', 'team_id', 'competition_id', unique=True),
    )
    
    def __repr__(self) -> str:
        return f"<TeamCompetition(team_id={self.team_id}, competition_id={self.competition_id})>"

