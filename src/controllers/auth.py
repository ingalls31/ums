from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from src.config.settings import SessionLocal
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session
from src.services import subjects as subjects_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth",],
    responses={404: {"description": "Not found"}},
)

