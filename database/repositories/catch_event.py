from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.catch_event import CatchEvent
from database.db import get_db_session


class CatchEventRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(CatchEvent, db_session)


def get_catch_event_repo(
    session=Depends(get_db_session),
) -> CatchEventRepository:
    """Catch event repository dependency"""
    return CatchEventRepository(session)
