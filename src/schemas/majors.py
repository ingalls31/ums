from typing import Optional
from pydantic import BaseModel, EmailStr


class MajorBaseSchema(BaseModel):
    name: str
    department: str
    description: Optional[str] = None
    total: Optional[int] = None

    class Config:
        from_attributes = True

class MajorSchema(MajorBaseSchema):
    id: str
