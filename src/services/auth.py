from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Union
from jose import JWTError, jwt
from uuid import UUID

from src.config import settings

from src.models.users import User
from src.schemas.auth import TokenData, RegisterUser
from src.util.auth import get_password_hash, verify_password, credentials_exception, create_refresh_token, validate_refresh_token, get_current_user_dep
from src.util.db_dependency import get_db

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = float(str(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
REFRESH_TOKEN_EXPIRE_MINUTES = float(str(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class InvalidUserException(Exception):
    """
    Exception raised when a user is not found in the database.
    """

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def get_user(db: Session, email: Union[str, None] = None):

    try:
        if email is None:
            raise InvalidUserException(status_code=404, detail="Email not provided")

        user_query = db.query(User).where(User.email == email)
        user = user_query.first()

        if not user:
            raise InvalidUserException(status_code=404, detail="User not found")
        print("user", user)
        return user
    except InvalidUserException:
        raise
    except Exception as e:
        print("Exception", e)
        raise InvalidUserException(status_code=400, detail=str(e))


def db_signup_users(
    user_data: RegisterUser, db: Session
):
    # Check if user already exists
    try:
        existing_user_email_query = db.query(User).filter(User.email == user_data.email)
        existing_user_email = existing_user_email_query.first()
        if existing_user_email:
            raise InvalidUserException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user instance
        new_user = User(
            email=user_data.email,
            password=hashed_password,
        )

        # Add new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return the new user data
        return new_user
    except InvalidUserException:
        raise
    except Exception as e:
        print("Exception", e)
        raise InvalidUserException(status_code=400, detail=str(e))


def authenticate_user(db, email: str, password: str):
    """
    Authenticates a user by checking if the provided email and password match the stored credentials.

    Args:
        db: The database object used for querying user information.
        email (str): The email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        user: The authenticated user object if the credentials are valid, False otherwise.
    """
    try: 
        user = get_user(db, email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except InvalidUserException:
        raise


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create an access token using the provided data and expiration delta.

    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (Union[timedelta, None], optional): The expiration delta for the access token.
            Defaults to None.

    Returns:
        str: The encoded access token.
    """
    try:
        to_encode = data.copy()
        # Convert UUID to string if it's present in the data
        if 'id' in to_encode and isinstance(to_encode['id'], UUID):
            to_encode['id'] = str(to_encode['id'])

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta

        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=1)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, str(
            SECRET_KEY), algorithm=str(ALGORITHM))

        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:  Annotated[Session, Depends(get_db)]):
    """
    Get the current authenticated user based on the provided token.

    Args:
        token (str): The authentication token.
        db (Session): The database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the credentials cannot be validated.
    """
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, str(SECRET_KEY),
                             algorithms=[str(ALGORITHM)])
        email: Union[str, None] = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    try:
        user = get_user(db, email=token_data.email)
        if user is None:
            raise credentials_exception
        return user
    except InvalidUserException:
        raise credentials_exception


async def service_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:  Annotated[Session, Depends(get_db)]
):
    """
    Authenticates the user and generates an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the email and password.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the access token, token type, and user information.
    """
    try:
        user = authenticate_user(db, form_data.email, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=float(str(ACCESS_TOKEN_EXPIRE_MINUTES)))
        access_token = create_access_token(
            data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
        )

        # Generate refresh token (you might want to set a longer expiry for this)
        refresh_token_expires = timedelta(
            minutes=float(str(REFRESH_TOKEN_EXPIRE_MINUTES)))
        refresh_token = create_refresh_token(
            data={"sub": user.email, "id": user.id}, expires_delta=refresh_token_expires)

        return {"access_token": access_token, "token_type": "bearer", "user": user, "expires_in": int(access_token_expires.total_seconds()), "refresh_token": refresh_token}
    except InvalidUserException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def service_signup_users(
    user_data: RegisterUser, db:  Annotated[Session, Depends(get_db)]
):
    """
    Service function to sign up users.

    Args:
        user_data (RegisterUser): The user data to be registered.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        The result of the user registration.

    Raises:
        HTTPException: If there is an invalid user exception or any other unforeseen exception.
    """
    try:
        return await db_signup_users(user_data, db)
    except InvalidUserException as e:
        # Catch the InvalidUserException and raise an HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Handle other unforeseen exceptions
        raise HTTPException(status_code=500, detail=str(e))


async def gpt_tokens_service(grant_type: str = Form(...), refresh_token: Optional[str] = Form(None), code: Optional[str] = Form(None)):
    """
    Generates access and refresh tokens based on the provided grant type.

    Args:
        grant_type (str): The grant type, either "refresh_token" or "authorization_code".
        refresh_token (str, optional): The refresh token used for token refresh flow.
        code (str, optional): The authorization code used for initial token generation flow.

    Returns:
        dict: A dictionary containing the access token, token type, expiry time, and refresh token.

    Raises:
        credentials_exception: If the grant type is invalid or the required parameters are missing.
    """
    # Token refresh flow
    if grant_type == "refresh_token":
        # Check if the refresh token is Present
        if not refresh_token:
            raise credentials_exception
        # Validate the refresh token and client credentials
        user_id = await validate_refresh_token(refresh_token)
        if not user_id:
            raise credentials_exception

    # Initial token generation flow
    elif grant_type == "authorization_code":
        user_id = await get_current_user_dep(code) 
        if not user_id:
            raise credentials_exception
    else:
        raise credentials_exception

    # Generate access token
    access_token_expires = timedelta(
        minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"id": user_id}, expires_delta=access_token_expires)

    # Generate refresh token (you might want to set a longer expiry for this)
    refresh_token_expires = timedelta(
        minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    rotated_refresh_token = create_refresh_token(
        data={"id": user_id}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "refresh_token": rotated_refresh_token  # Include refresh token in the response
    }