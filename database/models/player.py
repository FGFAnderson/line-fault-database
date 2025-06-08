from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import BaseModel
from sqlalchemy import Enum as SQLEnum
from ..enums.country_codes import CountryCode

if TYPE_CHECKING:
    from player_team_history import PlayerTeamHistory


# If data becomes larger we could implement height and dominant arm
class Player(BaseModel):
    """Player who is plays in competitions for various teams"""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    nationality: Mapped[Optional[str]] = mapped_column(SQLEnum(CountryCode))

    team_history: Mapped[list["PlayerTeamHistory"]] = relationship(
        back_populates="player"
    )

    def __repr__(self) -> str:
        return f"<Player(id={self.id}, first_name='{self.first_name}' last_name='{self.last_name}' country_code='{self.nationality}')>"
