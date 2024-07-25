from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.schemas.departments import DepartmentBaseSchema, DepartmentSchema
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import departments as departments_service

router = APIRouter(
    prefix="/departments",
    tags=["Departments",],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=DepartmentSchema)
def create_department(
    department_data: DepartmentBaseSchema,
    db: Session = Depends(get_db)
):
    """
    Create a new department.

    Args:
        department_data (DepartmentBaseSchema): The department object containing the department details.
        db (Session): The database session.

    Returns:
        DepartmentSchema: The created department object.
    """
    department = departments_service.create_department(department_data, db)
    return department


@router.get("/", response_model=List[DepartmentSchema])
def get_departments(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
):
    """
    Get all departments from the database with optional filtering by name.

    Args:
        db (Session): The database session.
        name (str, optional): Name filter.

    Returns:
        List[DepartmentSchema]: The list of DepartmentSchema objects representing all departments.
    """
    filters = {"name": name}
    departments = departments_service.get_filtered_departments(db, filters)
    return departments


@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department(
    department_id: str,
    db: Session = Depends(get_db),
) -> DepartmentSchema:
    """
    Retrieve a department from the database by its ID.

    Args:
        department_id (str): The ID of the department to be retrieved.
        db (Session): The database session.

    Returns:
        DepartmentSchema: The department object with the given ID.
    """
    department = departments_service.get_department_by_id(db, department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a department by its ID.

    Args:
        department_id (str): The ID of the department to be deleted.
        db (Session): The database session.

    Returns:
        None
    """
    departments_service.delete_department(db, department_id)
    
    return JSONResponse(status_code=204)
    


@router.patch("/{department_id}", response_model=DepartmentBaseSchema)
def update_department(department_id: str, data: DepartmentBaseSchema, db: Session = Depends(get_db)):
    """
    Update a department by its ID.

    Args:
        department_id (str): The ID of the department to be updated.
        data (DepartmentBaseSchema): The updated department data.
        db (Session): The database session.

    Returns:
        DepartmentBaseSchema: The updated department object.
    """
    updated_department = departments_service.update_department(db, department_id, data)
    return updated_department
