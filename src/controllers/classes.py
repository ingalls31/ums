from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.schemas.classes import ClassBaseSchema, ClassSchema
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import classes as classes_service

router = APIRouter(
    prefix="/classes",
    tags=["Classes",],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=ClassSchema)
def create_class(
    class_data: ClassBaseSchema,
    db: Session = Depends(get_db)
) -> ClassSchema:
    """
    Create a new class.

    Args:
        class_data (ClassBaseSchema): The class details.
        db (Session): The database session.

    Returns:
        ClassSchema: The created class object.
    """
    created_class = classes_service.create_class(class_data, db)
    return created_class


@router.get("/", response_model=List[ClassSchema])
def get_classes(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
) -> List[ClassSchema]:
    """
    Get all classes from the database with optional filtering by name.

    Args:
        db (Session): The database session.
        name (str, optional): Name filter.

    Returns:
        List[ClassSchema]: The list of ClassSchema objects representing all classes.
    """
    filters = {"name": name}
    classes = classes_service.get_filtered_classes(db, filters)
    return classes


@router.get("/{class_id}", response_model=ClassSchema)
def get_class_by_id(
    class_id: str,
    db: Session = Depends(get_db),
) -> ClassSchema:
    """
    Get a class by its ID.

    Args:
        class_id (str): The ID of the class to be retrieved.
        db (Session): The database session.

    Returns:
        ClassSchema: The class object with the given ID.

    Raises:
        HTTPException: If the class is not found.
    """
    class_obj = classes_service.get_class_by_id(db, class_id)
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


@router.delete("/{class_id}", status_code=204)
def delete_class_(class_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a class by its ID.

    Args:
        class_id (str): The ID of the class to be deleted.
        db (Session): The database session.
    """
    classes_service.delete_class(db, class_id)
    
    return JSONResponse(status_code=204)


@router.patch("/{class_id}", response_model=ClassBaseSchema)
def update_class(
    class_id: str,
    data: ClassBaseSchema,
    db: Session = Depends(get_db),
) -> ClassBaseSchema:
    """Update a class by its ID."""
    updated_class = classes_service.update_class(db, class_id, data)
    return updated_class
