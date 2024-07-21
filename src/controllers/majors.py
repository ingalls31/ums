from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.database import SessionLocal
from src.schemas.majors import MajorBaseSchema, MajorSchema
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import majors as majors_service

router = APIRouter(
    prefix="/majors",
    tags=["Majors",],
    responses={404: {"description": "Not found"}},
)




@router.post("/", response_model=MajorSchema)
def create_major(
    major_data: MajorBaseSchema,
    db: Session = Depends(get_db)
) -> MajorSchema:
    """
    Create a new major.

    Args:
        major_data (MajorBaseSchema): The major object containing the major details.
        db (Session): The database session.

    Returns:
        MajorSchema: The created major object.
    """
    major = majors_service.create_major(major_data, db)
    return major


@router.get("/", response_model=list[MajorSchema])
def get_majors(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
):
    """Retrieve all majors from the database with optional filtering by name."""
    filters = {"name": name}
    majors = majors_service.get_filtered_majors(db, filters)
    return majors


@router.get("/{major_id}", response_model=MajorSchema)
def get_major_by_id(
    major_id: str,
    db: Session = Depends(get_db),
) -> MajorSchema:
    """
    Retrieve a major from the database by its ID.

    Args:
        major_id (str): The ID of the major to be retrieved.
        db (Session): The database session.

    Returns:
        MajorSchema: The major object with the given ID.
    """
    major = majors_service.get_major_by_id(db, major_id)
    if major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    return major


@router.delete("/{major_id}", status_code=204)
def delete_major(major_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a major by its ID.

    Args:
        major_id (str): The ID of the major to be deleted.
        db (Session): The database session.

    Returns:
        None
    """
    majors_service.delete_major_by_id(db, major_id)


@router.patch("/{major_id}", response_model=MajorBaseSchema)
def update_major(major_id: str, data: MajorBaseSchema, db: Session = Depends(get_db)):
    """
    Update a major by its ID.

    Args:
        major_id (str): The ID of the major to be updated.
        data (MajorBaseSchema): The updated major data.
        db (Session): The database session.

    Returns:
        MajorBaseSchema: The updated major object.
    """
    updated_major = majors_service.update_major_by_id(db, major_id, data)
    return updated_major
