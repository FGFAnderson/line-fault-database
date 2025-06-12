from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.elimination_event import EliminationEvent
from database.db import get_db_session


class EliminationEventRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(EliminationEvent, db_session)


def get_elimination_event_repo(
    session=Depends(get_db_session),
) -> EliminationEventRepository:
    """Elimination event repository dependency"""
    return EliminationEventRepository(session)
