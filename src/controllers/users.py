from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.database import SessionLocal
from src.util.db_dependency import get_db
from src.services.users import *
from src.schemas.users import UserBaseSchema, UserSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=UserBaseSchema)
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
    # Convert the UserSchema object to a User object
    # Creating a new user object from the UserSchema object
    new_user = User(**vars(user))

    # Add the new user to the database session
    # Adding the new user to the database session
    db.add(new_user)

    # Commit the changes to the database
    # Committing the changes to the database
    db.commit()

    # Refresh the new user object with the generated ID and other database values
    # Refreshing the new user object with the generated ID and other database values
    db.refresh(new_user)

    # Return the created user object
    return new_user

@router.get("/", response_model=List[UserSchema])
def get_all_users(
    db: Session = Depends(get_db),
    email: Optional[str] = Query(None, description="Filter by email"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    address: Optional[str] = Query(None, description="Filter by address")
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
    query = db.query(User)

    # Apply filters if provided
    if email:
        query = query.filter(User.email == email)
    if gender:
        query = query.filter(User.gender == gender)
    if phone:
        query = query.filter(User.phone == phone)
    if address:
        query = query.filter(User.address == address)

    # Execute the query and get all users matching the filters
    users = query.all()

    # Return the list of users
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get a user by ID.

    Args:
        user_id (str): The ID of the user.
        db (Session): The database session.

    Returns:
        UserSchema: The user object.

    Raises:
        HTTPException: If the user is not found.
    """
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()
    
    # Raise an exception if the user is not found
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the user object
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    Args:
        user_id (str): The ID of the user to be deleted.
        db (Session): The database session.

    Returns:
        HTTP status code 204 (No Content) on successful deletion.

    Raises:
        HTTPException: If the user is not found.
    """
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()

    # Raise an exception if the user is not found
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database
    db.delete(user)
    db.commit()

    # Return an empty response with status code 204 (No Content)
    return {}

@router.patch("/{user_id}", response_model=UserBaseSchema)
def update_user(user_id: str, data: UserBaseSchema, db: Session = Depends(get_db)):
    """
    Partially update a user by their ID.

    Args:
        user_id (str): The ID of the user to be updated.
        data (UserBaseSchema): The data to update, specified as partial schema.
        db (Session): The database session.

    Returns:
        UserBaseSchema: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()

    # If the user does not exist, raise an exception
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user with the provided data
    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(user, key, value)

    # Commit the changes to the database
    db.commit()

    # Refresh the updated user object
    db.refresh(user)

    return user
