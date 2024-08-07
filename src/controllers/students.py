from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.models.users import User
from src.schemas.students import StudentBaseSchema, StudentSchema
from src.util.auth import current_admin, current_user
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import students as students_service

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=StudentSchema)
def create_student(
    student_data: StudentBaseSchema,
    user: Annotated[User, Depends(current_admin)], 
    db: Session = Depends(get_db)
):
    """
    Create a new student.

    Args:
        student_data (StudentBaseSchema): The student object containing the student details.
        db (Session): The database session.

    Returns:
        StudentSchema: The created student object.
    """
    student = students_service.create_student(student_data, db)
    return student


@router.get("/", response_model=List[StudentSchema])
def get_students(
    user: Annotated[User, Depends(current_admin)], 
    db: Session = Depends(get_db),
    code: Optional[str] = Query(None, description="Filter by code"),
):
    """
    Get all students from the database with optional filtering by code.

    Args:
        db (Session): The database session.
        code (str, optional): Code filter.

    Returns:
        List[StudentSchema]: The list of StudentSchema objects representing all students.
    """
    filters = {"code": code}
    students = students_service.get_filtered_students(db, filters)
        
    return students


@router.get("/{student_id}", response_model=StudentSchema)
def get_student(
    user: Annotated[User, Depends(current_user)], 
    student_id: str,
    db: Session = Depends(get_db),
) -> StudentSchema:
    """
    Retrieve a student from the database by their ID.

    Args:
        student_id (str): The ID of the student to be retrieved.
        db (Session): The database session.

    Returns:
        StudentSchema: The student object with the given ID.
    """
    student = students_service.get_student_by_id(db, student_id, user)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(
    user: Annotated[User, Depends(current_admin)], 
    student_id: str, 
    db: Session = Depends(get_db)
):
    """
    Delete a student by their ID.

    Args:
        student_id (str): The ID of the student to be deleted.
        db (Session): The database session.

    Returns:
        None
    """
    students_service.delete_student(db, student_id)
    
    return JSONResponse(status_code=204)
    


@router.patch("/{student_id}", response_model=StudentBaseSchema)
def update_student(
    student_id: str, 
    user: Annotated[User, Depends(current_user)], 
    data: StudentBaseSchema, 
    db: Session = Depends(get_db)
):
    """
    Update a student by their ID.

    Args:
        student_id (str): The ID of the student to be updated.
        data (StudentBaseSchema): The updated student data.
        db (Session): The database session.

    Returns:
        StudentBaseSchema: The updated student object.
    """
    updated_student = students_service.update_student(db, student_id, data, user)
    return updated_student
