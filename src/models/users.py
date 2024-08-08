import string
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.majors import Major
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(length=30), nullable=True)
    last_name = Column(String(length=30), nullable=True)
    email = Column(String(length=100))
    password = Column(String(length=250))
    gender = Column(String(length=10), nullable=True)
    phone = Column(String(length=20), nullable=True)
    dob = Column(String(length=30), nullable=True)
    address = Column(String(length=250), nullable=True)
    super_admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    
    
class Student(Base): 
    __tablename__ = 'students'
    
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(length=10))
    user_id = Column(String, ForeignKey(User.id, ondelete='CASCADE'))
    gpa = Column(Integer)
    major = Column(String, ForeignKey(Major.id, ondelete='CASCADE'))
    
    
class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(length=10))
    user_id = Column(String, ForeignKey(User.id, ondelete='CASCADE'))
    major = Column(String, ForeignKey(Major.id, ondelete='CASCADE'))
    
