import string
import uuid
from src.config.settings import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime


class Department(Base):
    __tablename__ = 'departments'

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(length=30))
    description = Column(String(length=250))
    total = Column(Integer)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=None)
    
    
