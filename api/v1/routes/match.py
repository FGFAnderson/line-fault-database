from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.match import (
    MatchRepository,
    get_match_repo,
)
from database.repositories.team import get_team_repo, TeamRepository
from api.v1.schemas.match import (
    MatchResponse,
    MatchCreate,
    MatchUpdate,
)

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[MatchResponse])
def read_all(
    repo: MatchRepository = Depends(get_match_repo),
) -> list[MatchResponse]:
    """Gets all of the matches

    Args:
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).

    Returns:
        list[MatchResponse]: A list of all matches in db
    """

    all_matches = repo.get_all()

    return all_matches


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    repo: MatchRepository = Depends(get_match_repo),
) -> MatchResponse:
    """Gets one match based on id

    Args:
        match_id (int): The match's ID
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).

    Raises:
        HTTPException_404: Match not found from ID

    Returns:
        MatchResponse: A match
    """

    match = repo.get_one(id=match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with ID {match_id} not found",
        )
    return match


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    match_data: MatchCreate,
    repo: MatchRepository = Depends(get_match_repo),
    team_repo: TeamRepository = Depends(get_team_repo),
) -> MatchResponse:
    """Creates a match

    Args:
        match_data (MatchCreate): A dictionary or any compatible type to be deconstructed into a **kwarg
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).
        team_repo (TeamRepository, optional): A object of the TeamRepo to validate teams exist. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Team not found
        HTTPException_400: Teams cannot play against themselves
        HTTPException_500: Generic failure from inner method

    Returns:
        MatchResponse: The created match
    """
    # Validate teams exist
    team1 = team_repo.get_one(id=match_data.team1_id)
    if not team1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {match_data.team1_id} not found",
        )

    team2 = team_repo.get_one(id=match_data.team2_id)
    if not team2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {match_data.team2_id} not found",
        )

    # Ensure teams are different
    if match_data.team1_id == match_data.team2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team cannot play against itself",
        )

    match_dict = match_data.model_dump()
    new_match = repo.create(**match_dict)

    if not new_match:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create match",
        )

    return new_match


@router.put("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: int,
    match_data: MatchUpdate,
    repo: MatchRepository = Depends(get_match_repo),
    team_repo: TeamRepository = Depends(get_team_repo),
) -> MatchResponse:
    """Updated a match based on its ID

    Args:
        match_id (int): The match's ID
        match_data (MatchUpdate): The fields to be updated
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).
        team_repo (TeamRepository, optional): A object of the TeamRepo to validate teams exist. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Match to update or team not found
        HTTPException_400: Teams cannot play against themselves
        HTTPException_500: Internal server error

    Returns:
        MatchResponse: The updated object
    """
    # Get the existing match
    existing_match = repo.get_one(id=match_id)
    if not existing_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with ID {match_id} not found",
        )

    # Get update data excluding unset fields
    update_data = match_data.model_dump(exclude_unset=True)

    # Validate teams if they're being updated
    team1_id = update_data.get("team1_id", existing_match.team1_id)
    team2_id = update_data.get("team2_id", existing_match.team2_id)

    # Check if teams exist (only if being updated)
    if "team1_id" in update_data:
        team1 = team_repo.get_one(id=team1_id)
        if not team1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team1_id} not found",
            )

    if "team2_id" in update_data:
        team2 = team_repo.get_one(id=team2_id)
        if not team2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team2_id} not found",
            )

    # Ensure teams are different
    if team1_id == team2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team cannot play against itself",
        )

    # Update the match
    updated_match = repo.update(existing_match, **update_data)

    if not updated_match:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update match",
        )

    return updated_match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    match_id: int,
    repo: MatchRepository = Depends(get_match_repo),
) -> None:
    """Deletes one match based on ID

    Args:
        match_id (int): The match's ID
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).

    Raises:
        HTTPException_404: Match to be deleted not found
        HTTPException_500: Internal server error
    """
    # Get the existing match
    existing_match = repo.get_one(id=match_id)
    if not existing_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with ID {match_id} not found",
        )

    # Delete the match
    deleted_match = repo.delete(existing_match)
    if not deleted_match:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete match",
        )


# Additional endpoints for filtering matches
@router.get("/competition/{competition_id}", response_model=list[MatchResponse])
def get_matches_by_competition(
    competition_id: int,
    repo: MatchRepository = Depends(get_match_repo),
) -> list[MatchResponse]:
    """Gets all matches for a specific competition

    Args:
        competition_id (int): The competition's ID
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).

    Returns:
        list[MatchResponse]: A list of matches for the competition
    """
    matches = repo.get_all(competition_id=competition_id)
    return matches


@router.get("/team/{team_id}", response_model=list[MatchResponse])
def get_matches_by_team(
    team_id: int,
    repo: MatchRepository = Depends(get_match_repo),
    team_repo: TeamRepository = Depends(get_team_repo),
) -> list[MatchResponse]:
    """Gets all matches for a specific team

    Args:
        team_id (int): The team's ID
        repo (MatchRepository, optional): A object of the MatchRepo that handles DB actions. Defaults to Depends(get_match_repo).
        team_repo (TeamRepository, optional): A object of the TeamRepo to validate team exists. Defaults to Depends(get_team_repo).

    Raises:
        HTTPException_404: Team not found

    Returns:
        list[MatchResponse]: A list of matches for the team
    """
    # Validate team exists
    team = team_repo.get_one(id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    # Get matches where team is either team1 or team2
    # Note: This uses your CRUDRepository's get_all method with conditional filters
    # You might need to enhance the base repository to handle OR conditions
    team1_matches = repo.get_all(team1_id=team_id)
    team2_matches = repo.get_all(team2_id=team_id)

    # Combine and deduplicate
    all_matches = team1_matches + team2_matches
    unique_matches = {match.id: match for match in all_matches}.values()

    return list(unique_matches)
