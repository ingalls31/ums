from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.majors import Major
from src.schemas.majors import MajorBaseSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create_major(major_data: MajorBaseSchema, db: Session) -> Major:
    """
    Creates a new major in the database.

    Args:
        major_data (MajorBaseSchema): The major object containing the major details.
        db (Session): The database session.

    Returns:
        Major: The created major object.

    Raises:
        Exception: If major creation fails.
    """
    try:
        new_major = Major(**major_data.dict())
        db.add(new_major)
        db.commit()
        db.refresh(new_major)
        return new_major
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Failed to create major: {error}")


def get_filtered_majors(db: Session, filters: dict[str, Any]) -> List[Major]:
    """
    Get majors from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Major to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Major]: A list of Major objects that match the given filters.
    """
    try:
        query = db.query(Major).filter(Major.deleted_at.is_(None))

        for attribute, value in filters.items():
            if value is not None:
                if attribute == 'name':
                    query = query.filter(getattr(Major, attribute).like(f"%{value}%"))
                else:
                    query = query.filter(getattr(Major, attribute) == value)

        return query.all()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")


def get_major_by_id(db: Session, major_id: str) -> Major:
    """
    Get a major from the database by its ID.

    Args:
        db (Session): The database session.
        major_id (str): The ID of the major to be retrieved.

    Returns:
        Major: The major object with the given ID.

    Raises:
        HTTPException: If the major is not found or if a database error occurs.
    """
    try:
        major = db.query(Major).filter(Major.deleted_at.is_(None)).get(major_id)
        if major is None:
            raise HTTPException(status_code=404, detail="Major not found")
        return major
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {error}")


def delete_major_by_id(db: Session, major_id: str) -> None:
    """
    Delete a major from the database by its ID.

    Args:
        db (Session): The database session.
        major_id (str): The ID of the major to be deleted.

    Raises:
        HTTPException: If the major is not found or if a database error occurs.
    """
    try:
        major = db.query(Major).filter(Major.deleted_at.is_(None)).get(major_id)
        if major is None:
            raise HTTPException(status_code=404, detail="Major not found")
        major.deleted_at = datetime.datetime.utcnow()
        db.commit()
        
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {error}")


def update_major_by_id(db: Session, major_id: str, update_data: MajorBaseSchema) -> Major:
    """
    Update a major in the database by its ID.

    Args:
        db (Session): The database session.
        major_id (str): The ID of the major to be updated.
        update_data (MajorBaseSchema): The updated major data.

    Returns:
        Major: The updated major object if the update is successful.

    Raises:
        HTTPException: If the major is not found or if a database error occurs.
    """
    try:
        major = db.query(Major).filter(Major.deleted_at.is_(None)).get(major_id)

        if major is None:
            raise HTTPException(status_code=404, detail="Major not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(major, key, value)

        db.commit()
        db.refresh(major)
        return major

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")

