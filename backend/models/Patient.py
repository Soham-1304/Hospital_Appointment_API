from sqlalchemy import Column,Integer,String,Date
from sqlalchemy.orm import relationship

from backend.database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(120),nullable=False,unique=True)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(String(10))

    appointments = relationship("Appointment",back_populates="patient")
    