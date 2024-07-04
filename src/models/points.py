import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.subjects import Subject
from src.models.users import User


class Point(Base):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(Integer, ForeignKey(Subject.id, ondelete='CASCADE'), nullable=False)
    user = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    diligence = Column(Integer)
    test = Column(Integer)
    practice = Column(Integer)
    final = Column(Integer)
    