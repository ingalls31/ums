from pydantic import BaseModel, Field

from datetime import datetime
from uuid import uuid4, UUID

from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    email: str = Field( unique=True, index=True)

class RegisterUser(User):
    password: str

class UserOutput(User):
    id: UUID

class LoginResponse(Token):
    user: UserOutput
    expires_in: int
    refresh_token: str