from typing import Optional
from pydantic import BaseModel, EmailStr


class ClassBaseSchema(BaseModel):
    name: str
    teacher: str 
    subject: str
    description: Optional[str]
    total: int

    class Config:
        from_attributes = True

class ClassSchema(ClassBaseSchema):
    id: str
