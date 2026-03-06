from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship

from backend.database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),unique=True,nullable=False)
    floor_number = Column(Integer)
    doctors = relationship("Doctor",back_populates="department")