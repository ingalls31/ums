from typing import Optional
from pydantic import BaseModel, EmailStr


class SubjectBaseSchema(BaseModel):
    name: str
    major: str
    description: Optional[str] = None
    total: Optional[int] = None

    class Config:
        from_attributes = True

class SubjectSchema(SubjectBaseSchema):
    id: str
