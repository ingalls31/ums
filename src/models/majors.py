import string
import uuid
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.departments import Department



class Major(Base):
    __tablename__ = 'majors'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(length=30))
    total = Column(Integer)
    description = Column(String(length=250))
    department = Column(String, ForeignKey(Department.id, ondelete='CASCADE'), nullable=False)