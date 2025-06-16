from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.catch_event import CatchEventRepository, get_catch_event_repo
from api.v1.schemas.catch_event import (
    CatchEventResponse,
    CatchEventCreate,
    CatchEventUpdate,
)

router = APIRouter(prefix="/catch-events", tags=["catch-events"])


@router.get("/", response_model=list[CatchEventResponse])
def read_all(
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> list[CatchEventResponse]:
    """Gets all catch events

    Args:
        repo (CatchEventRepository): Repository that handles DB actions.

    Returns:
        list[CatchEventResponse]: A list of all catch events in db
    """
    all_catches = repo.get_all()
    return all_catches


@router.get("/{catch_id}", response_model=CatchEventResponse)
def get_catch_event(
    catch_id: int,
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> CatchEventResponse:
    """Gets one catch event based on id

    Args:
        catch_id (int): The catch event's ID
        repo (CatchEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Catch event not found

    Returns:
        CatchEventResponse: A catch event
    """
    catch_event = repo.get_one(id=catch_id)
    if not catch_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catch event with ID {catch_id} not found",
        )
    return catch_event


@router.get("/set/{set_id}", response_model=list[CatchEventResponse])
def get_catches_by_set(
    set_id: int,
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> list[CatchEventResponse]:
    """Gets all catch events for a specific set

    Args:
        set_id (int): The set's ID
        repo (CatchEventRepository): Repository that handles DB actions.

    Returns:
        list[CatchEventResponse]: A list of catch events for the specified set
    """
    catches = repo.get_all(set_id=set_id)
    return catches


@router.post(
    "/", response_model=CatchEventResponse, status_code=status.HTTP_201_CREATED
)
def create_catch_event(
    catch_data: CatchEventCreate,
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> CatchEventResponse:
    """Creates a catch event

    Args:
        catch_data (CatchEventCreate): Catch event data
        repo (CatchEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_500: Generic failure from inner method

    Returns:
        CatchEventResponse: The created catch event
    """
    catch_dict = catch_data.model_dump()
    new_catch = repo.create(**catch_dict)

    if not new_catch:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create catch event",
        )

    return new_catch


@router.put("/{catch_id}", response_model=CatchEventResponse)
def update_catch_event(
    catch_id: int,
    catch_data: CatchEventUpdate,
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> CatchEventResponse:
    """Updates a catch event based on its ID

    Args:
        catch_id (int): The catch event's ID
        catch_data (CatchEventUpdate): The fields to be updated
        repo (CatchEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Catch event not found
        HTTPException_500: Internal server error

    Returns:
        CatchEventResponse: The updated catch event
    """
    # Get the existing catch event
    existing_catch = repo.get_one(id=catch_id)
    if not existing_catch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catch event with ID {catch_id} not found",
        )

    # Update provided fields
    update_data = catch_data.model_dump(exclude_unset=True)
    updated_catch = repo.update(existing_catch, **update_data)

    if not updated_catch:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update catch event",
        )

    return updated_catch


@router.delete("/{catch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_catch_event(
    catch_id: int,
    repo: CatchEventRepository = Depends(get_catch_event_repo),
) -> None:
    """Deletes one catch event based on ID

    Args:
        catch_id (int): The catch event's ID
        repo (CatchEventRepository): Repository that handles DB actions.

    Raises:
        HTTPException_404: Catch event not found
        HTTPException_500: Internal server error
    """
    # Get the existing catch event
    existing_catch = repo.get_one(id=catch_id)
    if not existing_catch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catch event with ID {catch_id} not found",
        )

    # Delete the catch event
    deleted_catch = repo.delete(existing_catch)
    if not deleted_catch:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete catch event",
        )
