from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.throw_event import ThrowEvent
from database.db import get_db_session


class ThrowEventRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(ThrowEvent, db_session)


def get_throw_event_repo(
    session=Depends(get_db_session),
) -> ThrowEventRepository:
    """Throw event repository dependency"""
    return ThrowEventRepository(session)
