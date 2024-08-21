import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime

from src.models.classes import Class
from src.models.subjects import Subject
from src.models.users import Student, Teacher, User


class Point(Base):
    __tablename__ = 'points'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    class_id = Column(String, ForeignKey(Class.id, ondelete='CASCADE'), nullable=False)
    student_id = Column(String, ForeignKey(Student.id, ondelete='CASCADE'), primary_key=True)
    teacher_id = Column(String, ForeignKey(Teacher.id, ondelete='CASCADE'), nullable=False)
    diligence = Column(Integer)
    test = Column(Integer)
    practice = Column(Integer)
    final = Column(Integer)
    deleted_at = Column(DateTime, default=None)
    