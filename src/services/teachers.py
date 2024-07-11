from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.users import Teacher
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.teachers import TeacherBaseSchema


def create_teacher(teacher_data: TeacherBaseSchema, db: Session) -> Teacher:
    """
    Create a new teacher in the database.

    Args:
        teacher_data (TeacherBaseSchema): The teacher details.
        db (Session): The database session.

    Returns:
        Teacher: The created teacher object if successful.

    Raises:
        Exception: If teacher creation fails.
    """
    try:
        new_teacher = Teacher(**teacher_data.dict())
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return new_teacher
    
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception("Failed to create teacher")


def get_filtered_teachers(db: Session, filters: dict[str, Any]) -> List[Teacher]:
    """
    Get teachers from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Teacher to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Teacher]: A list of Teacher objects that match the given filters.
    
    Raises:
        ValueError: If an invalid attribute is used for filtering.
    """
    query = db.query(Teacher)

    for attribute, value in filters.items():
        if value is not None:
            try:
                query = query.filter(getattr(Teacher, attribute) == value)
            except AttributeError:
                raise ValueError(f"Invalid attribute for filtering: {attribute}")
    
    return query.all()


def get_teacher_by_id(db: Session, teacher_id: str) -> Teacher:
    """
    Get a teacher from the database by their ID.

    Args:
        db (Session): The database session.
        teacher_id (str): The ID of the teacher to be retrieved.

    Returns:
        Teacher: The teacher object with the given ID.

    Raises:
        HTTPException: If the teacher is not found or if a database error occurs.
    """
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return teacher
    
    except SQLAlchemyError as error:
        raise Exception("Database error occurred: {}".format(error))


def delete_teacher(db: Session, teacher_id: str) -> None:
    """
    Delete a teacher from the database by their ID.

    Args:
        db (Session): The database session.
        teacher_id (str): The ID of the teacher to be deleted.

    Raises:
        HTTPException: If the teacher is not found or if a database error occurs.
    """
    try:
        teacher = db.query(Teacher).get(teacher_id)
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        db.delete(teacher)
        db.commit()
        
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")


def update_teacher(db: Session, teacher_id: str, update_data: TeacherBaseSchema) -> Teacher:
    """
    Update a teacher in the database by their ID.

    Args:
        db (Session): The database session.
        teacher_id (str): The ID of the teacher to be updated.
        update_data (TeacherBaseSchema): The updated teacher data.

    Returns:
        Teacher: The updated teacher object if the update is successful.

    Raises:
        HTTPException: If the teacher is not found or if a database error occurs.
    """
    try:
        teacher = db.query(Teacher).get(teacher_id)

        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")

        for attribute, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(teacher, attribute, value)

        db.commit()
        db.refresh(teacher)
        return teacher

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")
