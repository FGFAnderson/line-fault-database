from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.set import Set
from database.db import get_db_session


class SetRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(Set, db_session)


def get_set_repo(
    session=Depends(get_db_session),
) -> SetRepository:
    """Set repository dependency"""
    return SetRepository(session)
