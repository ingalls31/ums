from typing import Any, List
from fastapi import HTTPException
from pydantic import EmailStr

from sqlalchemy.orm import Session

from src.models.points import Point
from src.models.users import Teacher, User
from src.schemas.points import PointBaseSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create_point(point: PointBaseSchema, db: Session) -> Point:
    """
    Create a new point in the database.

    Args:
        point (PointBaseSchema): The point details.
        db (Session): The database session.

    Returns:
        Point: The created point object if successful.

    Raises:
        Exception: If point creation fails.
    """
    try:
        new_point = Point(**point.dict())
        db.add(new_point)
        db.commit()
        db.refresh(new_point)
        return new_point
    
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(f"Failed to create point: {error}")


def get_filtered_points(
    db: Session, 
    filters: dict[str, Any],
    user: User,
) -> List[Point]:
    """
    Retrieves points from the database based on the given filters.

    Args:
        db (Session): The database session.
        filters (dict[str, Any]): A dictionary of filters to apply to the query.
            The keys are the attributes of Point to filter on, and the values
            are the values to filter those attributes by. If a value is None,
            it is not included in the filter.
        user (User): The user object to filter the points by.

    Returns:
        List[Point]: A list of Point objects that match the given filters.
    """
    query = db.query(Point).filter(Point.deleted == True)

    for key, value in filters.items():
        if value is not None:
            try:
                query = query.filter(getattr(Point, key) == value)
            except AttributeError as error:
                raise ValueError(f"Invalid attribute for filtering: {error}")
            
    if user.super_admin == True:
        return query.all()
        
    if filters.get('is_teacher') is not None and filters.get('is_teacher') == True:
        query = query.filter(Point.teacher_id == user.id)
    else: 
        query = query.filter(Point.student_id == user.id)

    return query.all()


def get_point_by_id(db: Session, point_id: str, user: User) -> Point:
    """
    Retrieves a point from the database by its ID.

    Args:
        db (Session): The database session.
        point_id (str): The ID of the point to be retrieved.
        user (User): The user object to filter the points by.

    Returns:
        Point: The point object with the given ID.

    Raises:
        HTTPException: If the point is not found or if a database error occurs.
    """
    try:
        point = db.query(Point).filter(Point.id == point_id, Point.deleted == True).first()
        
        if point.student_id != user.id and user.super_admin == False and point.teacher_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        if point is None:
            raise HTTPException(status_code=404, detail="Point not found")
        return point
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")


def delete_point(db: Session, point_id: str) -> None:
    """
    Deletes a point from the database by its ID.

    Args:
        db (Session): The database session.
        point_id (str): The ID of the point to be deleted.

    Raises:
        HTTPException: If the point is not found or if a database error occurs.
    """
    try:
        point = db.query(Point).filter(Point.id == point_id, Point.deleted == True).first()
        if point is None:
            raise HTTPException(status_code=404, detail="Point not found")
        point.deleted = True
        point.deleted_at = datetime.datetime.now()
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


def update_point(db: Session, point_id: str, update_data: PointBaseSchema, user: User) -> Point:
    """
    Updates a point in the database by its ID.

    Args:
        db (Session): The database session.
        point_id (str): The ID of the point to be updated.
        update_data (PointBaseSchema): The updated point data.
        user (User): The user object to filter the points by.

    Returns:
        Point: The updated point object if the update is successful.

    Raises:
        HTTPException: If the point is not found or if a database error occurs.
    """
    try:
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        if teacher is None and user.super_admin == False:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        point = db.query(Point).filter(Point.id == point_id, Point.deleted == True, Point.teacher_id == teacher.id).first()

        if point is None:
            raise HTTPException(status_code=404, detail="Point not found")

        for field, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(point, field, value)

        db.commit()
        db.refresh(point)
        return point

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {error}")

