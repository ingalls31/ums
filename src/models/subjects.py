import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.majors import Major



class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    total = Column(Integer, default=0)
    major = Column(Integer, ForeignKey(Major.id, ondelete='CASCADE'), nullable=False)
    
    