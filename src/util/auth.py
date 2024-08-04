
import sqlalchemy.orm
import uuid
from fastapi import Depends, Form, HTTPException, status, Security
from fastapi.security import HTTPBearer, OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Any
from uuid import UUID

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from src.services import users as users_service

from src.config import settings
from src.util.db_dependency import get_db
from sqlalchemy.orm import Session


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

security = HTTPBearer()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

async def get_current_user_dep(bearer=Depends(security), db: Session = Depends(get_db) ):
    token = bearer.credentials
    try:
        if not token:
            raise credentials_exception
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[str(ALGORITHM)])
        user_id: str = str(payload.get("id"))
        # You can add more user-related validation here if needed
        return users_service.get_user_by_id(db, user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

    
# Function to verify refresh token
async def validate_refresh_token(refresh_token: str) -> Union[str, None]:
    try:

        payload: dict[str, Any] = jwt.decode(refresh_token, str(SECRET_KEY), algorithms=[str(ALGORITHM)])
        user_id: Union[str, None] = payload.get("id")

        # If user_id is None, the token is invalid
        if not user_id:
            return None

        return user_id
    except JWTError:
        return None
    
def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    # Convert UUID to string if it's present in the data
    if 'id' in to_encode and isinstance(to_encode['id'], UUID):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)  # Set the expiration time for refresh tokens to 7 days

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=str(ALGORITHM))

    return encoded_jwt

# Create a custom credentials exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW-Authenticate": 'Bearer'},
    detail={"error": "invalid_token", "error_description": "The access token expired"}
)