from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.throw_event import (
    ThrowEventRepository,
    get_throw_event_repo,
)
from api.v1.schemas.throw_event import (
    ThrowEventResponse,
    ThrowEventCreate,
    ThrowEventUpdate,
)

router = APIRouter(prefix="/throw-events", tags=["throw-events"])


@router.get("/", response_model=list[ThrowEventResponse])
def read_all(
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> list[ThrowEventResponse]:
    """Gets all throw events

    Args:
        repo (ThrowEventRepository): Repository that handles DB actions.

    Returns:
        list[ThrowEventResponse]: A list of all throw events in db
    """
    all_throws = repo.get_all()
    return all_throws


@router.get("/{throw_id}", response_model=ThrowEventResponse)
def get_throw_event(
    throw_id: int,
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> ThrowEventResponse:
    """Gets one throw event based on id

    Args:
        throw_id (int): The throw event's ID
        repo (ThrowEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Throw event not found

    Returns:
        ThrowEventResponse: A throw event
    """
    throw_event = repo.get_one(id=throw_id)
    if not throw_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Throw event with ID {throw_id} not found",
        )
    return throw_event


@router.get("/set/{set_id}", response_model=list[ThrowEventResponse])
def get_throws_by_set(
    set_id: int,
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> list[ThrowEventResponse]:
    """Gets all throw events for a specific set

    Args:
        set_id (int): The set's ID
        repo (ThrowEventRepository): Repository that handles DB actions.

    Returns:
        list[ThrowEventResponse]: A list of throw events for the specified set
    """
    throws = repo.get_all(set_id=set_id)
    return throws


@router.post(
    "/", response_model=ThrowEventResponse, status_code=status.HTTP_201_CREATED
)
def create_throw_event(
    throw_data: ThrowEventCreate,
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> ThrowEventResponse:
    """Creates a throw event

    Args:
        throw_data (ThrowEventCreate): Throw event data
        repo (ThrowEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_500: Generic failure from inner method

    Returns:
        ThrowEventResponse: The created throw event
    """
    throw_dict = throw_data.model_dump()
    new_throw = repo.create(**throw_dict)

    if not new_throw:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create throw event",
        )

    return new_throw


@router.put("/{throw_id}", response_model=ThrowEventResponse)
def update_throw_event(
    throw_id: int,
    throw_data: ThrowEventUpdate,
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> ThrowEventResponse:
    """Updates a throw event based on its ID

    Args:
        throw_id (int): The throw event's ID
        throw_data (ThrowEventUpdate): The fields to be updated
        repo (ThrowEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Throw event not found
        HTTPException_500: Internal server error

    Returns:
        ThrowEventResponse: The updated throw event
    """
    # Get the existing throw event
    existing_throw = repo.get_one(id=throw_id)
    if not existing_throw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Throw event with ID {throw_id} not found",
        )

    # Update provided fields
    update_data = throw_data.model_dump(exclude_unset=True)
    updated_throw = repo.update(existing_throw, **update_data)

    if not updated_throw:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update throw event",
        )

    return updated_throw


@router.delete("/{throw_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_throw_event(
    throw_id: int,
    repo: ThrowEventRepository = Depends(get_throw_event_repo),
) -> None:
    """Deletes one throw event based on ID

    Args:
        throw_id (int): The throw event's ID
        repo (ThrowEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Throw event not found
        HTTPException_500: Internal server error
    """
    # Get the existing throw event
    existing_throw = repo.get_one(id=throw_id)
    if not existing_throw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Throw event with ID {throw_id} not found",
        )

    # Delete the throw event
    deleted_throw = repo.delete(existing_throw)
    if not deleted_throw:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete throw event",
        )
