from typing import List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.users import Student
from src.schemas.students import StudentBaseSchema
from sqlalchemy.exc import SQLAlchemyError


def create_student(student: StudentBaseSchema, db: Session) -> Student:
    """
    Creates a new student in the database.

    Args:
        student (StudentBaseSchema): The student object containing the student details.
        db (Session): The database session.

    Returns:
        Student: The created student object if successful; None if an error occurs.

    Raises:
        Exception: Descriptive error if student creation fails.
    """
    try:
        new_student = Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to create student: {e}")


def get_filtered_students(db: Session, filters: dict) -> List[Student]:
    """
    Get students from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict): A dictionary of filters to apply to the query.
            The keys are the attributes of Student to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Student]: A list of Student objects that match the given filters.
    
    Raises:
        ValueError: If an invalid attribute is used for filtering.
        Exception: If there is an unexpected error during the query.
    """
    query = db.query(Student)
    try:
        for attribute, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Student, attribute) == value)
        return query.all()
    except AttributeError as e:
        raise ValueError(f"Invalid attribute for filtering: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def get_student_by_id(db: Session, student_id: str) -> Student:
    """
    Get a student from the database by their ID.

    Args:
        db (Session): The database session.
        student_id (str): The ID of the student to be retrieved.

    Returns:
        Student: The student object with the given ID.

    Raises:
        HTTPException: If the student is not found or if a database error occurs.
    """
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except SQLAlchemyError as error:
        raise Exception(f"Database error occurred: {error}")
    
    except Exception as error:
        raise Exception(f"An unexpected error occurred: {error}")


def delete_student(db: Session, student_id: str) -> None:
    """
    Delete a student from the database by their ID.

    Args:
        db (Session): The database session.
        student_id (str): The ID of the student to be deleted.

    Raises:
        HTTPException: If the student is not found or if a database error occurs.
    """
    try:
        student = db.query(Student).get(student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Database error occurred: {error}")
    
    except Exception as error:
        raise Exception(f"An unexpected error occurred: {error}")


def update_student_by_id(db: Session, student_id: str, update_data: StudentBaseSchema) -> Student:
    """
    Update a student in the database by their ID.

    Args:
        db (Session): The database session.
        student_id (str): The ID of the student to be updated.
        update_data (StudentBaseSchema): The updated student data.

    Returns:
        Student: The updated student object if the update is successful.

    Raises:
        HTTPException: If the student is not found or if a database error occurs.
    """
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        for key, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return student
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Database error occurred: {error}")
    
    except Exception as error:
        raise Exception(f"An unexpected error occurred: {error}")

