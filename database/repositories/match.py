from database.crud.base import CRUDRepository
from sqlalchemy.orm import Session
from database.db import get_db_session
from database.models.match import Match
from fastapi import Depends


class MatchRepository(CRUDRepository):
    """Repository for Match operations"""

    def __init__(self, db_session: Session):
        super().__init__(Match, db_session)


def get_match_repo(
    session=Depends(get_db_session),
) -> MatchRepository:
    """Match repository dependency"""
    return MatchRepository(session)
