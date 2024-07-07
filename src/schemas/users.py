import src.schemas.users
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    super_admin: Optional[bool] = False
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True
