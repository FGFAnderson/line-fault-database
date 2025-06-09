import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from database.models.organisation import Organisation
from database.repositories.organisation_repo import (
    OrganisationRepository,
    get_organisation_repo,
)
from schemas.organisation import OrganisationResponse

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("/all", response_model=list[OrganisationResponse])
def read_all(
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> Any:
    """
    Retrieve items.
    """

    all_orgs = repo.get_all()

    return all_orgs
