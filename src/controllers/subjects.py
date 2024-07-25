from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.schemas.subjects import SubjectBaseSchema, SubjectSchema
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import subjects as subjects_service

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects",],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=SubjectBaseSchema)
def create_subject(
    subject_data: SubjectBaseSchema,
    db: Session = Depends(get_db)
):
    """
    Create a new subject.

    Args:
        subject_data (SubjectBaseSchema): The subject object containing the subject details.
        db (Session): The database session.

    Returns:
        SubjectBaseSchema: The created subject object.
    """
    created_subject = subjects_service.create_subject(subject_data, db)
    return created_subject


@router.get("/", response_model=List[SubjectSchema])
def get_subjects(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
):
    """Get all subjects from the database with optional filtering by name."""
    filters = {"name": name}
    subjects = subjects_service.get_filtered_subjects(db, filters)
    return subjects


@router.get("/{subject_id}", response_model=SubjectSchema)
def get_subject_by_id(
    subject_id: str,
    db: Session = Depends(get_db),
) -> SubjectSchema:
    """
    Retrieve a subject from the database by its ID.

    Args:
        subject_id (str): The ID of the subject to be retrieved.
        db (Session): The database session.

    Returns:
        SubjectSchema: The subject object with the given ID.

    Raises:
        HTTPException: If the subject is not found.
    """
    subject = subjects_service.get_subject_by_id(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.delete("/{subject_id}", status_code=204)
def delete_subject(subject_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a subject by its ID.

    Args:
        subject_id (str): The ID of the subject to be deleted.
        db (Session): The database session.
    """
    subjects_service.delete_subject(db, subject_id)
    
    return JSONResponse(status_code=204)
    


@router.patch("/{subject_id}", response_model=SubjectBaseSchema)
def update_subject(
    subject_id: str,
    data: SubjectBaseSchema,
    db: Session = Depends(get_db),
) -> SubjectBaseSchema:
    """
    Update a subject by its ID.

    Args:
        subject_id (str): The ID of the subject to be updated.
        data (SubjectBaseSchema): The updated subject data.
        db (Session): The database session.

    Returns:
        SubjectBaseSchema: The updated subject object.
    """
    updated_subject = subjects_service.update_subject(db, subject_id, data)
    return updated_subject
