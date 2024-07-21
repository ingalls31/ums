from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.classes import Class
from src.schemas.classes import ClassBaseSchema
from sqlalchemy.exc import SQLAlchemyError


def create_class(class_data: ClassBaseSchema, db: Session) -> Class:
    """
    Create a new class in the database.

    Args:
        class_data (ClassBaseSchema): The class details.
        db (Session): The database session.

    Returns:
        Class: The created class object.

    Raises:
        Exception: If class creation fails.
    """
    new_class = Class(**class_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def get_filtered_classs(db: Session, filters: dict[str, Any]) -> List[Class]:
    """
    Get classs from the database that match the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Class to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.

    Returns:
        List[Class]: A list of Class objects that match the given filters.
    """
    query = db.query(Class)

    for key, value in filters.items():
        if value is not None:
            try:
                if key == 'name':
                    query = query.filter(getattr(Class, key).like(f"%{value}%"))
                else:
                    query = query.filter(getattr(Class, key) == value)
            except AttributeError as error:
                raise ValueError(f"Invalid attribute for filtering: {error}")

    return query.all()


def get_class_by_id(db: Session, class_id: str) -> Class:
    """
    Get a class from the database by its ID.

    Args:
        db (Session): The database session.
        class_id (str): The ID of the class to be retrieved.

    Returns:
        Class: The class object with the given ID.

    Raises:
        HTTPException: If the class is not found or if a database error occurs.
    """
    class_obj = db.query(Class).get(class_id)
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


def delete_class_(db: Session, class_id: str) -> None:
    """
    Delete a class from the database by its ID.

    Args:
        db (Session): The database session.
        class_id (str): The ID of the class to be deleted.

    Raises:
        HTTPException: If the class is not found or if a database error occurs.
    """
    class_to_delete = db.query(Class).get(class_id)

    if class_to_delete is None:
        raise HTTPException(status_code=404, detail="Class not found")

    db.delete(class_to_delete)
    db.commit()


def update_class(db: Session, class_id: str, update_data: ClassBaseSchema) -> Class:
    """
    Update a class in the database by its ID.

    Args:
        db (Session): The database session.
        class_id (str): The ID of the class to be updated.
        update_data (ClassBaseSchema): The updated class data.

    Returns:
        Class: The updated class object if the update is successful.

    Raises:
        HTTPException: If the class is not found or if a database error occurs.
    """
    class_obj = db.query(Class).get(class_id)

    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(class_obj, field, value)

    db.commit()
    db.refresh(class_obj)

    return class_obj
