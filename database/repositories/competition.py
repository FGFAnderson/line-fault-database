from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.competition import Competition
from database.db import get_db_session


class CompetitionRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(Competition, db_session)


def get_competition_repo(
    session=Depends(get_db_session),
) -> CompetitionRepository:
    """Competition repository dependency"""
    return CompetitionRepository(session)
