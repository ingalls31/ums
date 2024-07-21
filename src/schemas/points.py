from typing import Optional
from pydantic import BaseModel, EmailStr


class PointBaseSchema(BaseModel):
    subject: str 
    user: str
    diligence: int 
    test: int 
    practice: int
    final: int

    class Config:
        from_attributes = True

class PointSchema(PointBaseSchema):
    id: str
