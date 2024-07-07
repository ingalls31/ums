import src.schemas.users
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    super_admin: Optional[bool] = False
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class UserSchema(UserBaseSchema):
    id: str
