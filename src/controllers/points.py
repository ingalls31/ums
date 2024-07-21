from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.database import SessionLocal
from src.schemas.points import PointBaseSchema, PointSchema
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import points as points_service

router = APIRouter(
    prefix="/points",
    tags=["Points",],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=PointSchema)
def create_point(
    point_data: PointBaseSchema,
    db: Session = Depends(get_db)
):
    """
    Create a new point.

    Args:
        point_data (PointBaseSchema): The point object containing the point details.
        db (Session): The database session.

    Returns:
        PointSchema: The created point object.
    """
    point = points_service.create_point(point_data, db)
    return point


@router.get("/", response_model=List[PointSchema])
def get_points(
    db: Session = Depends(get_db),
    subject_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
) -> List[PointSchema]:
    """
    Retrieves all points from the database, optionally filtered by subject and user IDs.

    Args:
        db (Session): The database session.
        subject_id (str, optional): The ID of the subject to filter by.
        user_id (str, optional): The ID of the user to filter by.

    Returns:
        List[PointSchema]: A list of PointSchema objects representing the retrieved points.
    """
    filters = {
        "subject": subject_id,
        "user": user_id,
    }
    points = points_service.get_filtered_points(db, filters)
    return points


@router.get("/{point_id}", response_model=PointSchema)
def get_point(
    point_id: str,
    db: Session = Depends(get_db),
) -> PointSchema:
    """
    Retrieve a point from the database by its ID.

    Args:
        point_id (str): The ID of the point to be retrieved.
        db (Session): The database session.

    Returns:
        PointSchema: The point object with the given ID.
    """
    point = points_service.get_point_by_id(db, point_id)
    if point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return point


@router.delete("/{point_id}", status_code=204)
def delete_point(point_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a point by its ID.

    Args:
        point_id (str): The ID of the point to be deleted.
        db (Session): The database session.

    Returns:
        None
    """
    points_service.delete_point(db, point_id)
    
    return JSONResponse(status_code=204)


@router.patch("/{point_id}", response_model=PointBaseSchema)
def update_point(point_id: str, data: PointBaseSchema, db: Session = Depends(get_db)):
    """
    Update a point by its ID.

    Args:
        point_id (str): The ID of the point to be updated.
        data (PointBaseSchema): The updated point data.
        db (Session): The database session.

    Returns:
        PointBaseSchema: The updated point object.
    """
    updated_point = points_service.update_point(db, point_id, data)
    return updated_point
