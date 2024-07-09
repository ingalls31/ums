from typing import List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.users import User
from src.schemas.users import UserBaseSchema
from sqlalchemy.exc import SQLAlchemyError


def create_user(user: UserBaseSchema, db: Session) -> User:
    """
    Creates a new user in the database.

    Args:
        user (UserBaseSchema): The user object containing the user details.
        db (Session): The database session.

    Returns:
        User: The created user object if successful; None if an error occurs.

    Raises:
        Exception: Descriptive error if user creation fails.
    """
    try:
        new_user = User(**vars(user))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to create user: {e}")


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
        
    Raises:
        Exception: Descriptive error if there is a problem during the query.
    """
    try:
        query = db.query(User)

        for key, value in filters.items():
            if value is not None:
                try:
                    query = query.filter(getattr(User, key) == value)
                except AttributeError:
                    raise ValueError(f"Invalid attribute for filtering: {key}")
        return query.all()

    except SQLAlchemyError as e:
        raise Exception(f"Database error occurred: {e}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def get_user_by_id(db: Session, user_id: str) -> User:
    """
    Get a user from the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be retrieved.

    Returns:
        User: The user object with the given ID.

    Raises:
        HTTPException: If the user is not found or if a database error occurs.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    except SQLAlchemyError as e:
       raise Exception(f"Database error occurred: {e}")
   
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def delete_user_by_id(db: Session, user_id: str) -> None:
    """
    Delete a user from the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be deleted.

    Raises:
        HTTPException: If the user is not found or if a database error occurs.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error occurred: {e}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def update_user_by_id(db: Session, user_id: str, update_data: UserBaseSchema) -> User:
    """
    Update a user in the database by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to be updated.
        update_data (UserBaseSchema): The updated user data.

    Returns:
        User: The updated user object if the update is successful.

    Raises:
        HTTPException: If the user is not found or if a database error occurs.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error occurred: {e}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")