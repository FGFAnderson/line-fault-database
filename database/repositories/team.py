from database.crud.base import CRUDRepository
from sqlalchemy.orm import Session
from database.db import get_db_session
from database.models.team import Team
from fastapi import Depends


class TeamRepository(CRUDRepository):
    """Repository for Team operations"""

    def __init__(self, db_session: Session):
        super().__init__(Team, db_session)


def get_team_repo(
    session=Depends(get_db_session),
) -> TeamRepository:
    """Team repository dependency"""
    return TeamRepository(session)
