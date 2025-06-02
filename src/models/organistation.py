from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import Enum as SQLEnum
from models.base import Base
from models.competition import Competition

class CountryCode(str, Enum):
    WLD = "WLD" # World country code for international events
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