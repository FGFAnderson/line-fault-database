from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.organisation_repo import (
    OrganisationRepository,
    get_organisation_repo,
)
from schemas.organisation import (
    OrganisationResponse,
    OrganisationCreate,
    OrganisationUpdate,
)

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("/", response_model=list[OrganisationResponse])
def read_all(
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> list[OrganisationResponse]:
    """Gets all of the organisations

    Args:
        repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Returns:
        list[OrganisationResponse]: A list of all organisations in db
    """

    all_orgs = repo.get_all()

    return all_orgs


@router.get("/{organisation_id}", response_model=OrganisationResponse)
def get_organisation(
    organisation_id: int,
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> OrganisationResponse:
    """Gets one organisation based on id

    Args:
        organisation_id (int): The organisation's ID
        repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_404: Organisation not found from ID

    Returns:
        OrganisationResponse: An organisation
    """

    organisation = repo.get_one(id=organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation with ID {organisation_id} not found",
        )
    return organisation


@router.post(
    "/", response_model=OrganisationResponse, status_code=status.HTTP_201_CREATED
)
def create_organisation(
    organisation_data: OrganisationCreate,
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> OrganisationResponse:
    """Creates an organisation

    Args:
        organisation_data (OrganisationCreate): A dictionary or any compatiable type to be deconstructed into a **kwarg
        repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_409: Duplicate Name, names must be unique
        HTTPException_500: Generic failure from inner method

    Returns:
        OrganisationResponse: The created organisation
    """
    # Check if organisation name is unique
    existing = repo.get_one(name=organisation_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Organisation with name '{organisation_data.name}' already exists",
        )

    org_dict = organisation_data.model_dump()
    new_organisation = repo.create(**org_dict)

    if not new_organisation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organisation",
        )

    return new_organisation


@router.put("/{organisation_id}", response_model=OrganisationResponse)
def update_organisation(
    organisation_id: int,
    organisation_data: OrganisationUpdate,
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> OrganisationResponse:
    """Updated an organisation based on it's ID

    Args:
        organisation_id (int): The organisation's ID
        organisation_data (OrganisationUpdate): The fields to be updated, these are unpacked so e.g name="Test", country_code="EN"
        repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_404: Organisation to update id is not found
        HTTPException_409: New name is not unique to other Organisations
        HTTPException_500: Internal server error

    Returns:
        OrganisationResponse: The updated object
    """
    # Get the existing organisation
    existing_org = repo.get_one(id=organisation_id)
    if not existing_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation with ID {organisation_id} not found",
        )

    # Check if name is unique
    if organisation_data.name and organisation_data.name != existing_org.name:
        name_conflict = repo.get_one(name=organisation_data.name)
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organisation with name '{organisation_data.name}' already exists",
            )

    # Update provided fields
    update_data = organisation_data.model_dump(exclude_unset=True)
    updated_org = repo.update(existing_org, **update_data)

    if not updated_org:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update organisation",
        )

    return updated_org


@router.delete("/{organisation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organisation(
    organisation_id: int,
    repo: OrganisationRepository = Depends(get_organisation_repo),
) -> None:
    """Deletes on organisation based on ID

    Args:
        organisation_id (int): The organisation's ID
        repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_404: Organisation to be deleted not found
        HTTPException_500: Internal server error
    """
    # Get the existing organisation
    existing_org = repo.get_one(id=organisation_id)
    if not existing_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation with ID {organisation_id} not found",
        )

    # Delete the organisation
    deleted_org = repo.delete(existing_org)
    if not deleted_org:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete organisation",
        )
