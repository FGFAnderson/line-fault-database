from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.elimination_event import (
    EliminationEventRepository,
    get_elimination_event_repo,
)
from api.v1.schemas.elimination_event import (
    EliminationEventResponse,
    EliminationEventCreate,
    EliminationEventUpdate,
)

router = APIRouter(prefix="/elimination-events", tags=["elimination-events"])


@router.get("/", response_model=list[EliminationEventResponse])
def read_all(
    repo: EliminationEventRepository = Depends(get_elimination_event_repo),
) -> list[EliminationEventResponse]:
    """Gets all elimination events

    Args:
        repo (EliminationEventRepository): Repository that handles DB actions.

    Returns:
        list[EliminationEventResponse]: A list of all elimination events in db
    """
    all_eliminations = repo.get_all()
    return all_eliminations


@router.get("/{elimination_id}", response_model=EliminationEventResponse)
def get_elimination_event(
    elimination_id: int,
    repo: EliminationEventRepository = Depends(get_elimination_event_repo),
) -> EliminationEventResponse:
    """Gets one elimination event based on id

    Args:
        elimination_id (int): The elimination event's ID
        repo (EliminationEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Elimination event not found

    Returns:
        EliminationEventResponse: An elimination event
    """
    elimination = repo.get_one(id=elimination_id)
    if not elimination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elimination event with ID {elimination_id} not found",
        )
    return elimination


@router.post(
    "/", response_model=EliminationEventResponse, status_code=status.HTTP_201_CREATED
)
def create_elimination_event(
    elimination_data: EliminationEventCreate,
    repo: EliminationEventRepository = Depends(get_elimination_event_repo),
) -> EliminationEventResponse:
    """Creates an elimination event

    Args:
        elimination_data (EliminationEventCreate): Elimination event data
        repo (EliminationEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_500: Generic failure from inner method

    Returns:
        EliminationEventResponse: The created elimination event
    """
    elimination_dict = elimination_data.model_dump()
    new_elimination = repo.create(**elimination_dict)

    if not new_elimination:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create elimination event",
        )

    return new_elimination


@router.put("/{elimination_id}", response_model=EliminationEventResponse)
def update_elimination_event(
    elimination_id: int,
    elimination_data: EliminationEventUpdate,
    repo: EliminationEventRepository = Depends(get_elimination_event_repo),
) -> EliminationEventResponse:
    """Updates an elimination event based on its ID

    Args:
        elimination_id (int): The elimination event's ID
        elimination_data (EliminationEventUpdate): The fields to be updated
        repo (EliminationEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Elimination event not found
        HTTPException_409: Player already eliminated in this set
        HTTPException_500: Internal server error

    Returns:
        EliminationEventResponse: The updated elimination event
    """
    # Get the existing elimination event
    existing_elimination = repo.get_one(id=elimination_id)
    if not existing_elimination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elimination event with ID {elimination_id} not found",
        )

    # Check for duplicate elimination if player or set is being changed
    if (
        elimination_data.eliminated_player_id is not None
        or elimination_data.set_id is not None
    ):
        new_player_id = (
            elimination_data.eliminated_player_id
            or existing_elimination.eliminated_player_id
        )
        new_set_id = elimination_data.set_id or existing_elimination.set_id

        # Only check if something actually changed
        if (
            new_player_id != existing_elimination.eliminated_player_id
            or new_set_id != existing_elimination.set_id
        ):
            duplicate_check = repo.get_one(
                set_id=new_set_id, eliminated_player_id=new_player_id
            )
            if duplicate_check and duplicate_check.id != elimination_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Player {new_player_id} is already eliminated in set {new_set_id}",
                )

    # Update provided fields
    update_data = elimination_data.model_dump(exclude_unset=True)
    updated_elimination = repo.update(existing_elimination, **update_data)

    if not updated_elimination:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update elimination event",
        )

    return updated_elimination


@router.delete("/{elimination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_elimination_event(
    elimination_id: int,
    repo: EliminationEventRepository = Depends(get_elimination_event_repo),
) -> None:
    """Deletes one elimination event based on ID

    Args:
        elimination_id (int): The elimination event's ID
        repo (EliminationEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Elimination event not found
        HTTPException_500: Internal server error
    """
    # Get the existing elimination event
    existing_elimination = repo.get_one(id=elimination_id)
    if not existing_elimination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elimination event with ID {elimination_id} not found",
        )

    # Delete the elimination event
    deleted_elimination = repo.delete(existing_elimination)
    if not deleted_elimination:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete elimination event",
        )
