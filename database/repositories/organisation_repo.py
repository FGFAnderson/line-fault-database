from typing import Generator
from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.organisation import Organisation
from sqlalchemy.orm import Session
from database.db import get_db_session


class OrganisationRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(Organisation, db_session)


def get_organisation_repo(
    db: Session = Depends(get_db_session),
) -> Generator[OrganisationRepository, None, None]:
    """Organisation repository dependency"""
    with db as session:
        yield OrganisationRepository(session)
