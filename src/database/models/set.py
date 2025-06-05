from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base import BaseModel

class Set(BaseModel):
    
    """ A set of dodgeball """
    
    __tablename__ = "sets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    set_number: Mapped[int] # This is required to avoid concurrency errors if we calculated it using the PK
    start_time: Mapped[datetime]
    end_time: Mapped[Optional[datetime]]
    
    winning_team_id: Mapped[Optional[int]]