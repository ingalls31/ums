from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.models.users import User
from src.schemas.teachers import TeacherBaseSchema, TeacherSchema
from src.util.auth import current_admin
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import teachers as teachers_service

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=TeacherSchema)
def create_teacher(
    teacher_data: TeacherBaseSchema,
    user: Annotated[User, Depends(current_admin)], 
    db: Session = Depends(get_db)
):
    """
    Create a new teacher.

    Args:
        teacher_data (TeacherBaseSchema): The teacher object containing the teacher details.
        db (Session): The database session.

    Returns:
        TeacherSchema: The created teacher object.
    """
    return teachers_service.create_student(teacher_data, db)


@router.get("/", response_model=List[TeacherSchema])
def get_teachers(
    user: Annotated[User, Depends(current_admin)], 
    db: Session = Depends(get_db),
    teacher_code: Optional[str] = Query(None, description="Filter by teacher code"),
):
    """
    Get all teachers from the database with optional filtering by teacher code.

    Args:
        db (Session): The database session.
        teacher_code (str, optional): Teacher code filter.

    Returns:
        List[TeacherSchema]: The list of TeacherSchema objects representing all teachers.
    """
    filters = {"code": teacher_code}
    teachers = teachers_service.get_filtered_teachers(db, filters)
    return teachers


@router.get("/{teacher_id}", response_model=TeacherSchema)
def get_teacher(
    user: Annotated[User, Depends(current_admin)], 
    teacher_id: str,
    db: Session = Depends(get_db),
) -> TeacherSchema:
    """
    Get a teacher by their ID.

    Args:
        teacher_id (str): The ID of the teacher to be retrieved.
        db (Session): The database session.

    Returns:
        TeacherSchema: The teacher object with the given ID.
    """
    teacher = teachers_service.get_teacher_by_id(db, teacher_id, user)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(
    user: Annotated[User, Depends(current_admin)], 
    teacher_id: str, 
    db: Session = Depends(get_db)) -> None:
    """
    Delete a teacher by their ID.

    Args:
        teacher_id (str): The ID of the teacher to be deleted.
        db (Session): The database session.

    Returns:
        None
    """
    teachers_service.delete_teacher(db, teacher_id)
    
    return JSONResponse(status_code=204)
    


@router.patch("/{teacher_id}", response_model=TeacherBaseSchema)
def update_teacher(
    user: Annotated[User, Depends(current_admin)], 
    teacher_id: str, 
    teacher_data: TeacherBaseSchema, 
    db: Session = Depends(get_db)):
    """
    Update a teacher by their ID.

    Args:
        teacher_id (str): The ID of the teacher to be updated.
        teacher_data (TeacherBaseSchema): The updated teacher data.
        db (Session): The database session.

    Returns:
        TeacherBaseSchema: The updated teacher object.
    """
    updated_teacher = teachers_service.update_teacher(db, teacher_id, teacher_data, user)
    return updated_teacher
