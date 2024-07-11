from typing import Optional
from pydantic import BaseModel, EmailStr


class DepartmentBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    total: Optional[int] = None

    class Config:
        from_attributes = True

class DepartmentSchema(DepartmentBaseSchema):
    id: str
