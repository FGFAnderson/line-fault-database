from fastapi import Depends
from database.crud.base import CRUDRepository
from database.models.organisation import Organisation
from database.db import get_db_session


class OrganisationRepository(CRUDRepository):
    def __init__(self, db_session):
        super().__init__(Organisation, db_session)


def get_organisation_repo(
    session=Depends(get_db_session),
) -> OrganisationRepository:
    """Organisation repository dependency"""
    return OrganisationRepository(session)
