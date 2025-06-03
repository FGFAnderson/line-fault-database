from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base import BaseModel

class SetEvent(BaseModel):
    
    __tablename__ = "set_events"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.id"))
    timestamp: Mapped[datetime]
    event_type: Mapped[str]
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    location_x: Mapped[Optional[float]]
    location_y: Mapped[Optional[float]]
