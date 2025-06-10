from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.team import (
    TeamRepository,
    get_team_repo,
)
from api.v1.schemas.team import (
    TeamResponse,
    TeamCreate,
    TeamUpdate,
)

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamResponse])
def read_all(
    repo: TeamRepository = Depends(get_team_repo),
) -> list[TeamResponse]:
    """Gets all of the teams

    Args:
        repo (TeamRepository, optional): A object of the TeamRepo that handles DB actions. Defaults to Depends(get_team_repo).

    Returns:
        list[TeamResponse]: A list of all teams in db
    """

    all_teams = repo.get_all()

    return all_teams


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    repo: TeamRepository = Depends(get_team_repo),
) -> TeamResponse:
    """Gets one team based on id

    Args:
        team_id (int): The team's ID
        repo (TeamRepository, optional): A object of the TeamRepo that handles DB actions. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Team not found from ID

    Returns:
        TeamResponse: A team
    """

    team = repo.get_one(id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )
    return team


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    repo: TeamRepository = Depends(get_team_repo),
) -> TeamResponse:
    """Creates a team

    Args:
        team_data (TeamCreate): A dictionary or any compatible type to be deconstructed into a **kwarg
        repo (TeamRepository, optional): A object of the TeamRepo that handles DB actions. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_409: Duplicate Name, names must be unique
        HTTPException_500: Generic failure from inner method

    Returns:
        TeamResponse: The created team
    """
    # Check if team name is unique
    existing = repo.get_one(name=team_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team_data.name}' already exists",
        )

    team_dict = team_data.model_dump()
    new_team = repo.create(**team_dict)

    if not new_team:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create team",
        )

    return new_team


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    repo: TeamRepository = Depends(get_team_repo),
) -> TeamResponse:
    """Updated a team based on its ID

    Args:
        team_id (int): The team's ID
        team_data (TeamUpdate): The fields to be updated, these are unpacked so e.g name="Test Team", logo_url="https://example.com/logo.png"
        repo (TeamRepository, optional): A object of the TeamRepo that handles DB actions. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Team to update id is not found
        HTTPException_409: New name is not unique to other Teams
        HTTPException_500: Internal server error

    Returns:
        TeamResponse: The updated object
    """
    # Get the existing team
    existing_team = repo.get_one(id=team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    # Check if name is unique
    if team_data.name and team_data.name != existing_team.name:
        name_conflict = repo.get_one(name=team_data.name)
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Team with name '{team_data.name}' already exists",
            )

    # Update provided fields
    update_data = team_data.model_dump(exclude_unset=True)
    updated_team = repo.update(existing_team, **update_data)

    if not updated_team:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update team",
        )

    return updated_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    repo: TeamRepository = Depends(get_team_repo),
) -> None:
    """Deletes one team based on ID

    Args:
        team_id (int): The team's ID
        repo (TeamRepository, optional): A object of the TeamRepo that handles DB actions. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Team to be deleted not found
        HTTPException_500: Internal server error
    """
    # Get the existing team
    existing_team = repo.get_one(id=team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    # Delete the team
    deleted_team = repo.delete(existing_team)
    if not deleted_team:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete team",
        )
