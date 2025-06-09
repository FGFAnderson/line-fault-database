from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.competition import (
    CompetitionRepository,
    get_competition_repo,
)
from database.repositories.organisation import (
    OrganisationRepository,
    get_organisation_repo,
)
from api.v1.schemas.competition import (
    CompetitionResponse,
    CompetitionCreate,
    CompetitionUpdate,
)

router = APIRouter(prefix="/competitions", tags=["competitions"])


@router.get("/", response_model=list[CompetitionResponse])
def read_all(
    repo: CompetitionRepository = Depends(get_competition_repo),
) -> list[CompetitionResponse]:
    """Gets all competitions

    Args:
        repo (CompetitionRepository, optional): A object of the CompetitionRepo that handles DB actions. Defaults to Depends(get_competition_repo).

    Returns:
        list[CompetitionResponse]: A list of all competitions in db
    """
    all_competitions = repo.get_all()
    return all_competitions


@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(
    competition_id: int,
    repo: CompetitionRepository = Depends(get_competition_repo),
) -> CompetitionResponse:
    """Gets one competition based on id

    Args:
        competition_id (int): The competition's ID
        repo (CompetitionRepository, optional): A object of the CompetitionRepo that handles DB actions. Defaults to Depends(get_competition_repo).

    Raises:
        HTTPException_404: Competition not found from ID

    Returns:
        CompetitionResponse: A competition
    """
    competition = repo.get_one(id=competition_id)
    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found",
        )
    return competition


@router.post(
    "/", response_model=CompetitionResponse, status_code=status.HTTP_201_CREATED
)
def create_competition(
    competition_data: CompetitionCreate,
    repo: CompetitionRepository = Depends(get_competition_repo),
    org_repo: OrganisationRepository = Depends(get_organisation_repo),
) -> CompetitionResponse:
    """Creates a competition

    Args:
        competition_data (CompetitionCreate): Competition data to create
        repo (CompetitionRepository, optional): A object of the CompetitionRepo that handles DB actions. Defaults to Depends(get_competition_repo).
        org_repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_404: Organisation not found
        HTTPException_409: Duplicate competition name for the same organisation
        HTTPException_500: Generic failure from inner method

    Returns:
        CompetitionResponse: The created competition
    """
    # Verify organisation exists
    organisation = org_repo.get_one(id=competition_data.organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation with ID {competition_data.organisation_id} not found",
        )

    # Check if competition name is unique within the organisation
    existing = repo.get_one(
        name=competition_data.name, organisation_id=competition_data.organisation_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Competition with name '{competition_data.name}' already exists for this organisation",
        )

    comp_dict = competition_data.model_dump()
    new_competition = repo.create(**comp_dict)

    if not new_competition:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create competition",
        )

    return new_competition


@router.put("/{competition_id}", response_model=CompetitionResponse)
def update_competition(
    competition_id: int,
    competition_data: CompetitionUpdate,
    repo: CompetitionRepository = Depends(get_competition_repo),
    org_repo: OrganisationRepository = Depends(get_organisation_repo),
) -> CompetitionResponse:
    """Updates a competition based on its ID

    Args:
        competition_id (int): The competition's ID
        competition_data (CompetitionUpdate): The fields to be updated
        repo (CompetitionRepository, optional): A object of the CompetitionRepo that handles DB actions. Defaults to Depends(get_competition_repo).
        org_repo (OrganisationRepository, optional): A object of the OrganisationRepo that handles DB actions. Defaults to Depends(get_organisation_repo).

    Raises:
        HTTPException_404: Competition or organisation not found
        HTTPException_409: New name is not unique within the organisation
        HTTPException_500: Internal server error

    Returns:
        CompetitionResponse: The updated competition
    """
    # Get the existing competition
    existing_comp = repo.get_one(id=competition_id)
    if not existing_comp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found",
        )

    # If organisation_id is being updated, verify the new organisation exists
    if (
        competition_data.organisation_id
        and competition_data.organisation_id != existing_comp.organisation_id
    ):
        organisation = org_repo.get_one(id=competition_data.organisation_id)
        if not organisation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organisation with ID {competition_data.organisation_id} not found",
            )

    # Check if name is unique within the organisation (considering potential organisation change)
    org_id = competition_data.organisation_id or existing_comp.organisation_id
    if competition_data.name and competition_data.name != existing_comp.name:
        name_conflict = repo.get_one(name=competition_data.name, organisation_id=org_id)
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Competition with name '{competition_data.name}' already exists for this organisation",
            )

    # Update provided fields
    update_data = competition_data.model_dump(exclude_unset=True)
    updated_comp = repo.update(existing_comp, **update_data)

    if not updated_comp:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update competition",
        )

    return updated_comp


@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competition(
    competition_id: int,
    repo: CompetitionRepository = Depends(get_competition_repo),
) -> None:
    """Deletes a competition based on ID

    Args:
        competition_id (int): The competition's ID
        repo (CompetitionRepository, optional): A object of the CompetitionRepo that handles DB actions. Defaults to Depends(get_competition_repo).

    Raises:
        HTTPException_404: Competition to be deleted not found
        HTTPException_500: Internal server error
    """
    # Get the existing competition
    existing_comp = repo.get_one(id=competition_id)
    if not existing_comp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} not found",
        )

    # Delete the competition
    deleted_comp = repo.delete(existing_comp)
    if not deleted_comp:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete competition",
        )

    return
