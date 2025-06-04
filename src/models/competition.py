from enum import Enum
from typing import TYPE_CHECKING, list
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from models.base import BaseModel

if TYPE_CHECKING:
    from models.organisation import Organisation
    from models.team_competition import TeamCompetition
    from models.match import Match

class CompetitionFormat(str, Enum):
    LEAGUE = "league"
    TOURNAMENT = "tournament"

class AgeCategory(str, Enum):
    U11 = "u11"
    U13 = "u13"
    U15 = "u15"
    U17 = "u17"
    ADULT = "adult"
    
class CourtSize(str, Enum):
    BD = "bd"
    EDF = "edf"
    NO_NEUTRAL_ZONE = "no_neutral_zone"

class Competition(BaseModel):
    """ A season or tournament """
    
    __tablename__ = "competitions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    competition_format: Mapped[CompetitionFormat] = mapped_column(SQLEnum(CompetitionFormat))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))
    organisation: Mapped["Organisation"] = relationship(back_populates="competitions")
    age_category: Mapped["AgeCategory"] = mapped_column(SQLEnum(AgeCategory))
    court_size: Mapped["CourtSize"] = mapped_column(SQLEnum(CourtSize))
    matches: Mapped[list["Match"]] = relationship(
        back_populates="competition",
        cascade="all, delete-orphan"
    )
    team_competitions: Mapped[list["TeamCompetition"]] = relationship(
        back_populates="competition",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Competition(id={self.id}, name='{self.name}', format='{self.competition_format}')>"
    