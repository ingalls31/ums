from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.database import SessionLocal
from src.util.db_dependency import get_db
from src.services.users import *
from src.schemas.users import UserBaseSchema, UserSchema
from src.services import users as users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=UserSchema)
def create_user(
    user: UserBaseSchema,  # UserSchema object representing the user to be created
    db: Session = Depends(get_db)  # Dependency injection for the database session
):
    """
    Create a new user.

    Args:
        user (UserSchema): The user object containing the user details.
        db (Session): The database session.

    Returns:
        UserSchema: The created user object.
    """
    return users_service.create_user(user, db)


@router.get("/", response_model=List[UserSchema])
def get_all_users(
    db: Session = Depends(get_db),  # Dependency injection for the database session
    email: Optional[str] = Query(None, description="Filter by email"),  # Query parameter for filtering by email
    gender: Optional[str] = Query(None, description="Filter by gender"),  # Query parameter for filtering by gender
    phone: Optional[str] = Query(None, description="Filter by phone number"),  # Query parameter for filtering by phone number
    address: Optional[str] = Query(None, description="Filter by address")  # Query parameter for filtering by address
):
    """
    Get all users from the database with optional filtering by email, gender, phone, and address.

    Args:
        db (Session): The database session.
        email (str, optional): Email filter.
        gender (str, optional): Gender filter.
        phone (str, optional): Phone filter.
        address (str, optional): Address filter.

    Returns:
        List[UserSchema]: The list of UserSchema objects representing all users.
    """
    # Start with a query object
    filters = {  # Dictionary of query parameters
        "email": email,
        "gender": gender,
        "phone": phone,
        "address": address
    }
    # Use the get_filtered_users service to get the filtered users
    users = users_service.get_filtered_users(db, filters)
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get a user by their ID.

    Args:
        user_id (str): The ID of the user to be retrieved.
        db (Session): The database session.

    Returns:
        UserSchema: The user object with the given ID.
    """
    # Get the user with the given ID from the database
    return users_service.get_user_by_id(db, user_id)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    Args:
        user_id (str): The ID of the user to be deleted.
        db (Session): The database session.

    Returns:
        dict: An empty dictionary.
    """
    # Delete the user with the given ID from the database
    users_service.delete_user_by_id(db, user_id)

    # Return an empty dictionary as the response body
    return JSONResponse(status_code=204)



@router.patch("/{user_id}", response_model=UserBaseSchema)
def update_user(user_id: str, data: UserBaseSchema, db: Session = Depends(get_db)):
    """
    Update a user by their ID.

    Args:
        user_id (str): The ID of the user to be updated.
        data (UserBaseSchema): The updated user data.
        db (Session): The database session.

    Returns:
        UserBaseSchema: The updated user object.
    """
    # Update the user with the given ID in the database with the provided data
    return users_service.update_user_by_id(db, user_id, data)
