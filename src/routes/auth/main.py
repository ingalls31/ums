"""Handling authentication and authorization"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from .service import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token,
    fake_users_db, is_user_disabled)
from .schemas import Token, EmailSchema, SetNewPassword
from src.util.db_dependency import get_db
from src.routes.users.services import check_user_existence_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    # if not check_user_existence_by_email(mail=form_data.username, db=db):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="There is no user with this email."
    #     )

    # if is_user_disabled(user_email=form_data.username, db=db):
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail="This user has been disabled. Login is not possible."
    #     )

    user = authenticate_user(username=form_data.username, password=form_data.password, db=fake_users_db)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
