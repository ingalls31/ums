from typing import List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.users import User
from src.schemas.users import UserBaseSchema



def create_user(user: UserBaseSchema, db: Session) -> User:
    """
    Creates a new user in the database.

    Args:
        user (UserBaseSchema): The user object containing the user details.
        db (Session): The database session.

    Returns:
        User: The created user object.

    Raises:
        None
    """
    # Create a new User object from the UserBaseSchema
    new_user = User(**vars(user))
    
    # Add the new user to the database session
    db.add(new_user)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the updated user object
    db.refresh(new_user)
    
    # Return the created user object
    return new_user

def get_filtered_users(db: Session, filters: dict) -> List[User]:
    """
    Get users from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict): A dictionary of filters to apply to the query.
            The keys are the attributes of User to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[User]: A list of User objects that match the given filters.
    """
    # Start with a query object for the User model
    query = db.query(User)

    # Iterate over the filters and add them to the query
    for key, value in filters.items():
        # If the value is not None, add a filter to the query
        if value is not None:
            query = query.filter(getattr(User, key) == value)

    # Execute the query and return the results
    return query.all()



def get_user_by_id(db: Session, user_id: str) -> User:
    """
    Get a user from the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be retrieved.

    Returns:
        User: The user object with the given ID.

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

def delete_user_by_id(db: Session, user_id: str) -> None:
    """
    Delete a user from the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be deleted.

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

    # Commit the changes to the database
    db.commit()


def update_user_by_id(db: Session, user_id: str, update_data: UserBaseSchema) -> User:
    """
    Update a user in the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be updated.
        update_data (UserBaseSchema): The updated user data.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()

    # Raise an exception if the user is not found
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's attributes with the provided data
    for key, value in update_data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(user, key, value)

    # Commit the changes to the database
    db.commit()

    # Refresh the updated user object
    db.refresh(user)

    # Return the updated user object
    return user
