from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Form, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.config.settings import SessionLocal
from src.models.users import User
from src.schemas.auth import  LoginResponse
from src.services.auth import service_login_for_access_token
from src.util.auth import current_user
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import subjects as subjects_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth",],
    responses={404: {"description": "Not found"}},
)



class OAuth2PasswordRequestFormCustom:
    def __init__(
        self, 
        email: str = Form(...), 
        password: str = Form(...)
    ):
        self.email = email
        self.password = password

@router.post("/login", response_model=LoginResponse)
async def login_authorization(form_data: Annotated[OAuth2PasswordRequestFormCustom, Depends()], db: Annotated[Session, Depends(get_db)]):
    """
    Authorization URL for Auth

    Args:
        form_data (Annotated[AuthPasswordRequestForm, Depends()]): Form Data
        db (Session, optional): Dependency Injection

    Returns:
        LoginResponse: Login Response
    """
    try: 
        return await service_login_for_access_token(form_data, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint that takes token and returns user data
@router.get("/me")
async def me(user: Annotated[User, Depends(current_user)]):
    """
    Get Current User

    Args:
        current_user (UserOutput, optional):  Dependency Injection

    Returns:
        UserOutput: User Output
    """
    return user