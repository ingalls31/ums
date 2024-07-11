from typing import Optional
from pydantic import BaseModel, EmailStr


class TeacherBaseSchema(BaseModel):
    code: str
    user: str
    major: Optional[str] = None

    class Config:
        from_attributes = True

class TeacherSchema(TeacherBaseSchema):
    id: str
