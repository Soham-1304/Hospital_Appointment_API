from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer,primary_key=True,index=True)
    appointment_id = Column(Integer,ForeignKey("appointments.id"),unique=True,nullable=False)
    diagnosis = Column(String(255))
    medicines = Column(String)
    instructions = Column(String)

    appointment = relationship("Appointment",back_populates="prescription")

