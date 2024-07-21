import string
import uuid
from src.config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey


class Department(Base):
    __tablename__ = 'departments'

    id = Column(String(length=36), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(length=30))
    description = Column(String(length=250))
    total = Column(Integer)
    
