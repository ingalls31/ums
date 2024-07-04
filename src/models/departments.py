import string
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30))
    description = Column(String(length=250))
    total = Column(Integer)
    
