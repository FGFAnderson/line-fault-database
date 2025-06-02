from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models.base import Base
from models.team_competition import TeamCompetition

class Team(Base):
    """ A team which competes in competitions """
    
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    
    team_competitions: Mapped[List["TeamCompetition"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}')>"