import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.routes.subjects.models import Subject
from src.routes.users.models import Teacher


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30))
    teacher = Column(Integer, ForeignKey(Teacher.id, ondelete='CASCADE'))
    subject = Column(Integer, ForeignKey(Subject.id, ondelete='CASCADE'))
    description = Column(String(length=250))
    total = Column(Integer)