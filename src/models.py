from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, SmallInteger, String, Index
from sqlalchemy import Enum as SQLEnum

class CountryCode(str, Enum):
    ENG = "ENG"
    SCO = "SCO"
    WAL = "WAL"
    NIR = "NIR"
    IRL = "IRL"
    GB = "GB"
    IN = "IN"
    CN = "CN"
    US = "US"
    ID = "ID"
    PK = "PK"
    NG = "NG"
    BR = "BR"
    BD = "BD"
    RU = "RU"
    ET = "ET"
    MX = "MX"
    JP = "JP"
    EG = "EG"
    PH = "PH"
    CD = "CD"
    VN = "VN"
    IR = "IR"
    TR = "TR"
    DE = "DE"
    TH = "TH"
    TZ = "TZ"
    FR = "FR"
    ZA = "ZA"
    IT = "IT"
    KE = "KE"
    MM = "MM"
    CO = "CO"
    KR = "KR"
    SD = "SD"
    UG = "UG"
    ES = "ES"
    DZ = "DZ"
    IQ = "IQ"
    AR = "AR"
    AF = "AF"
    YE = "YE"
    CA = "CA"
    AO = "AO"
    UA = "UA"
    MA = "MA"
    PL = "PL"
    UZ = "UZ"
    MY = "MY"
    MZ = "MZ"
    GH = "GH"
    PE = "PE"
    SA = "SA"
    MG = "MG"
    CI = "CI"

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
    
class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Base(DeclarativeBase):
    pass

class Organisation(Base):
    """ A league or tournament organiser """
    
    __tablename__ = "organisations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    country_code: Mapped[CountryCode] = mapped_column(SQLEnum(CountryCode))
    region: Mapped[Optional[str]] = mapped_column(String(100))
    website: Mapped[Optional[str]] = mapped_column(String(2048))
    logo_url: Mapped[Optional[str]] = mapped_column(String(2048))
    competitions: Mapped[List["Competition"]] = relationship(back_populates="organisation")
    
    def __repr__(self) -> str:
        return f"<Organisation(id={self.id}, name='{self.name}', country='{self.country_code}')>"

class Competition(Base):
    """ A season or tournament """
    
    __tablename__ = "competitions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    competition_format: Mapped[CompetitionFormat] = mapped_column(SQLEnum(CompetitionFormat))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))
    organisation: Mapped["Organisation"] = relationship(back_populates="competitions")
    age_category: Mapped["AgeCategory"] = mapped_column(SQLEnum(AgeCategory))
    court_size: Mapped["CourtSize"] = mapped_column(SQLEnum(CourtSize))
    matches: Mapped[List["Match"]] = relationship(
        back_populates="competition",
        cascade="all, delete-orphan"
    )
    team_competitions: Mapped[List["TeamCompetition"]] = relationship(
        back_populates="competition",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Competition(id={self.id}, name='{self.name}', format='{self.competition_format}')>"
    
    
class TeamCompetition(Base):
    """Junction table for teams participating in competitions"""
    __tablename__ = "team_competitions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"), nullable=False)
    joined_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utc)
    
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

class Match(Base):
    """ A match in a league or competion """
    
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    competition: Mapped["Competition"] = relationship(back_populates="matches")
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    team1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team1_score: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    team2_score: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    match_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped["MatchStatus"] = mapped_column(SQLEnum(MatchStatus))

    def __repr__(self) -> str:
        return f"<Match(id={self.id}, team1_id={self.team1_id}, team2_id={self.team2_id}, status='{self.status}')>"