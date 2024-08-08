import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.classes import Class
from src.models.subjects import Subject
from src.models.users import User


class Point(Base):
    __tablename__ = 'points'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    class_id = Column(String, ForeignKey(Class.id, ondelete='CASCADE'), nullable=False)
    user = Column(String, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    diligence = Column(Integer)
    test = Column(Integer)
    practice = Column(Integer)
    final = Column(Integer)
    