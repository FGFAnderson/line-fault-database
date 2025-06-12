from fastapi import APIRouter, Depends, HTTPException, status
from database.repositories.set import (
    SetRepository,
    get_set_repo,
)
from api.v1.schemas.set import (
    SetResponse,
    SetCreate,
    SetUpdate,
)

router = APIRouter(prefix="/sets", tags=["sets"])


@router.get("/", response_model=list[SetResponse])
def read_all(
    repo: SetRepository = Depends(get_set_repo),
) -> list[SetResponse]:
    """Gets all of the sets

    Args:
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Returns:
        list[SetResponse]: A list of all sets in db
    """

    all_sets = repo.get_all()

    return all_sets


@router.get("/{set_id}", response_model=SetResponse)
def get_set(
    set_id: int,
    repo: SetRepository = Depends(get_set_repo),
) -> SetResponse:
    """Gets one set based on id

    Args:
        set_id (int): The set's ID
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Raises:
        HTTPException_404: Set not found from ID

    Returns:
        SetResponse: A set
    """

    set_obj = repo.get_one(id=set_id)
    if not set_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with ID {set_id} not found",
        )
    return set_obj


@router.get("/match/{match_id}", response_model=list[SetResponse])
def get_sets_by_match(
    match_id: int,
    repo: SetRepository = Depends(get_set_repo),
) -> list[SetResponse]:
    """Gets all sets for a specific match

    Args:
        match_id (int): The match's ID
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Returns:
        list[SetResponse]: A list of sets for the specified match
    """

    sets = repo.get_all(match_id=match_id)
    return sets


@router.post("/", response_model=SetResponse, status_code=status.HTTP_201_CREATED)
def create_set(
    set_data: SetCreate,
    repo: SetRepository = Depends(get_set_repo),
) -> SetResponse:
    """Creates a set

    Args:
        set_data (SetCreate): A dictionary or any compatible type to be deconstructed into a **kwarg
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Raises:
        HTTPException_409: Duplicate set number for the same match
        HTTPException_500: Generic failure from inner method

    Returns:
        SetResponse: The created set
    """
    # Check if set number is unique for this match
    existing = repo.get_one(match_id=set_data.match_id, set_number=set_data.set_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Set number {set_data.set_number} already exists for match {set_data.match_id}",
        )

    set_dict = set_data.model_dump()
    new_set = repo.create(**set_dict)

    if not new_set:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create set",
        )

    return new_set


@router.put("/{set_id}", response_model=SetResponse)
def update_set(
    set_id: int,
    set_data: SetUpdate,
    repo: SetRepository = Depends(get_set_repo),
) -> SetResponse:
    """Updates a set based on its ID

    Args:
        set_id (int): The set's ID
        set_data (SetUpdate): The fields to be updated, these are unpacked so e.g match_id=1, set_number=2
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Raises:
        HTTPException_404: Set to update id is not found
        HTTPException_409: New set number is not unique for the match
        HTTPException_500: Internal server error

    Returns:
        SetResponse: The updated object
    """
    # Get the existing set
    existing_set = repo.get_one(id=set_id)
    if not existing_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with ID {set_id} not found",
        )

    # Check if set number is unique for the match
    if set_data.set_number is not None or set_data.match_id is not None:
        match_id = (
            set_data.match_id
            if set_data.match_id is not None
            else existing_set.match_id
        )
        set_number = (
            set_data.set_number
            if set_data.set_number is not None
            else existing_set.set_number
        )

        # Only check for conflicts if something actually changed
        if match_id != existing_set.match_id or set_number != existing_set.set_number:
            conflict = repo.get_one(match_id=match_id, set_number=set_number)
            if conflict and conflict.id != set_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Set number {set_number} already exists for match {match_id}",
                )

    # Update provided fields
    update_data = set_data.model_dump(exclude_unset=True)
    updated_set = repo.update(existing_set, **update_data)

    if not updated_set:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update set",
        )

    return updated_set


@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_set(
    set_id: int,
    repo: SetRepository = Depends(get_set_repo),
) -> None:
    """Deletes one set based on ID

    Args:
        set_id (int): The set's ID
        repo (SetRepository, optional): A object of the SetRepo that handles DB actions. Defaults to Depends(get_set_repo).

    Raises:
        HTTPException_404: Set to be deleted not found
        HTTPException_500: Internal server error
    """
    # Get the existing set
    existing_set = repo.get_one(id=set_id)
    if not existing_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with ID {set_id} not found",
        )

    # Delete the set
    deleted_set = repo.delete(existing_set)
    if not deleted_set:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete set",
        )
