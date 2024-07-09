from typing import Optional
from pydantic import BaseModel, EmailStr


class StudentBaseSchema(BaseModel):
    code: str
    user: str
    gpa: Optional[float] = None
    major: Optional[str] = None

    class Config:
        from_attributes = True

class StudentSchema(StudentBaseSchema):
    id: str
