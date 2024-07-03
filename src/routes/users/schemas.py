from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    gender: str
    phone: str
    dob: str
    address: str
    super_admin: bool
    disabled: bool | None = None

    class Config:
        from_attributes = True
