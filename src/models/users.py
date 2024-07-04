import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from src.models.majors import Major



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=30))
    last_name = Column(String(length=30))
    email = Column(String(length=100))
    password = Column(String(length=250))
    gender = Column(String(length=10))
    phone = Column(String(length=20))
    dob = Column(String(length=30))
    address = Column(String(length=250))
    super_admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    
class Student(Base): 
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(length=10))
    user = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    gpa = Column(Integer)
    major = Column(Integer, ForeignKey(Major.id, ondelete='CASCADE'))
    
class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(length=10))
    user = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    major = Column(Integer, ForeignKey(Major.id, ondelete='CASCADE'))
    
