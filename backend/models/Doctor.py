from sqlalchemy import Column,Integer,String,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    specialization = Column(String(100),index=True)
    consultation_fee = Column(Float)
    is_available = Column(Boolean,default=True)
    department_id = Column(Integer,ForeignKey("departments.id"))

    department = relationship("Department",back_populates="doctors")
    appointments = relationship("Appointment",back_populates="doctor")
    
