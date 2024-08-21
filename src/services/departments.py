from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.departments import Department
from src.schemas.departments import DepartmentBaseSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create_department(department: DepartmentBaseSchema, db: Session) -> Department:
    """
    Create a new department in the database.

    Args:
        department (DepartmentBaseSchema): The department details.
        db (Session): The database session.

    Returns:
        Department: The created department object if successful.

    Raises:
        Exception: If department creation fails.
    """
    try:
        new_department = Department(**department.dict())
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        return new_department
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Failed to create department: {error}")


def get_filtered_departments(db: Session, filters: dict[str, Any]) -> List[Department]:
    """
    Get departments from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Department to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Department]: A list of Department objects that match the given filters.
    """
    query = db.query(Department).filter(Department.deleted_at.is_(None))

    for key, value in filters.items():
        if value is not None:
            try:
                if key == 'name':
                    query = query.filter(getattr(Department, key).like(f"%{value}%"))
                else:
                    query = query.filter(getattr(Department, key) == value)
            except AttributeError as error:
                raise ValueError(f"Invalid attribute for filtering: {error}")

    try:
        result = query.all()
    except SQLAlchemyError as error:
        raise Exception(f"Failed to get filtered departments: {error}")

    return result


def get_department_by_id(db: Session, department_id: str) -> Department:
    """
    Get a department from the database by its ID.

    Args:
        db (Session): The database session.
        department_id (str): The ID of the department to be retrieved.

    Returns:
        Department: The department object with the given ID.

    Raises:
        HTTPException: If the department is not found or if a database error occurs.
    """
    try:
        department = db.query(Department).filter_by(id=department_id, deleted_at=None).first()
        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        return department
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")


def delete_department(db: Session, department_id: str) -> None:
    """
    Delete a department from the database by its ID.

    Args:
        db (Session): The database session.
        department_id (str): The ID of the department to be deleted.

    Raises:
        HTTPException: If the department is not found or if a database error occurs.
    """
    try:
        department = db.query(Department).filter_by(id=department_id).first()
        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        department.deleted_at = datetime.datetime.now()
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")


def update_department(db: Session, department_id: str, update_data: DepartmentBaseSchema) -> Department:
    """
    Update a department in the database by its ID.

    Args:
        db (Session): The database session.
        department_id (str): The ID of the department to be updated.
        update_data (DepartmentBaseSchema): The updated department data.

    Returns:
        Department: The updated department object if the update is successful.

    Raises:
        HTTPException: If the department is not found or if a database error occurs.
    """
    try:
        department = db.query(Department).filter_by(id=department_id, deleted_at=None).first()

        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")

        for field, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(department, field, value)

        db.commit()
        db.refresh(department)
        return department

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")

