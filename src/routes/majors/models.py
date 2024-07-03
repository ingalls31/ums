import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.routes.departments.models import Department


class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30))
    total = Column(Integer)
    description = Column(String(length=250))
    department = Column(Integer, ForeignKey(Department.id, ondelete='CASCADE'), nullable=False)