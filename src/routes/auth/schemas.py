from pydantic import BaseModel

from src.routes.users.models import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class EmailSchema(BaseModel):
    email: str


class SetNewPassword(BaseModel):
    user_id: int
    reset_token: str
    new_password: str


class Password(BaseModel):
    new_password: str
    
class UserInDB(User):
    hashed_password: str
