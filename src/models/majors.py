import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime

from src.models.departments import Department



class Major(Base):
    __tablename__ = 'majors'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(length=30))
    total = Column(Integer)
    description = Column(String(length=250))
    department_id = Column(String, ForeignKey(Department.id, ondelete='CASCADE'), nullable=False)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=None)
    