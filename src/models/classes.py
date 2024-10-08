import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime

from src.models.subjects import Subject
from src.models.users import Teacher


class Class(Base):
    __tablename__ = 'classes'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(length=30))
    teacher_id = Column(String, ForeignKey(Teacher.id, ondelete='CASCADE'))
    subject_id = Column(String, ForeignKey(Subject.id, ondelete='CASCADE'))
    description = Column(String(length=250))
    total = Column(Integer)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=None)