from enums.country_codes import CountryCode
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import Enum as SQLEnum
from models.base import BaseModel
from models.competition import Competition


class Organisation(BaseModel):
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