import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime

from src.models.majors import Major



class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    total = Column(Integer, default=0)
    major_id = Column(String, ForeignKey(Major.id, ondelete='CASCADE'), nullable=False)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=None)
    
    