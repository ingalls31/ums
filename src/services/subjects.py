from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.subjects import Subject
from src.schemas.subjects import SubjectBaseSchema
from sqlalchemy.exc import SQLAlchemyError


def create_subject(subject_data: SubjectBaseSchema, db: Session) -> Subject:
    """Create a new Subject in the database.

    Args:
        subject_data (SubjectBaseSchema): The Subject details.
        db (Session): The database session.

    Returns:
        Subject: The created Subject object if successful.

    Raises:
        Exception: If Subject creation fails.
    """
    try:
        new_subject = Subject(**subject_data.dict())
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        return new_subject
    
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Failed to create Subject: {error}")


def get_filtered_subjects(db: Session, filters: dict[str, Any]) -> List[Subject]:
    """
    Get subjects from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Subject to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Subject]: A list of Subject objects that match the given filters.
    """
    query = db.query(Subject)

    for attribute, value in filters.items():
        if value is not None:
            query = query.filter(getattr(Subject, attribute).like(f"%{value}%") if attribute == 'name'
                                 else getattr(Subject, attribute) == value)

    return query.all()


def get_subject_by_id(db: Session, subject_id: str) -> Subject:
    """
    Get a subject from the database by its ID.

    Args:
        db (Session): The database session.
        subject_id (str): The ID of the subject to be retrieved.

    Returns:
        Subject: The subject object with the given ID.

    Raises:
        HTTPException: If the subject is not found or if a database error occurs.
    """
    try:
        subject = db.query(Subject).get(subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")


def delete_subject(db: Session, subject_id: str) -> None:
    """
    Delete a subject from the database by its ID.

    Args:
        db (Session): The database session.
        subject_id (str): The ID of the subject to be deleted.

    Raises:
        HTTPException: If the subject is not found or if a database error occurs.
    """
    try:
        subject = db.query(Subject).get(subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        db.delete(subject)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


def update_subject(db: Session, subject_id: str, update_data: SubjectBaseSchema) -> Subject:
    """Update a subject in the database by its ID.

    Args:
        db (Session): The database session.
        subject_id (str): The ID of the subject to be updated.
        update_data (SubjectBaseSchema): The updated subject data.

    Returns:
        Subject: The updated subject object if the update is successful.

    Raises:
        HTTPException: If the subject is not found or if a database error occurs.
    """
    try:
        subject = db.query(Subject).get(subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")

        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(subject, field, value)

        db.commit()
        db.refresh(subject)
        return subject
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")

