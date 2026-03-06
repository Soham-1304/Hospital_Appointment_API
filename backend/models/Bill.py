from sqlalchemy import Column,Integer,String,Float,Enum,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.models.Enums import PaymentStatus

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer,primary_key=True,index=True)
    appointment_id = Column(Integer,ForeignKey("appointments.id"),unique=True,nullable=False)
    total_amount = Column(Float,nullable=False)
    payment_status = Column(Enum(PaymentStatus),default=PaymentStatus.PENDING,nullable=False)
    generated_at = Column(DateTime,default=datetime.now)

    appointment = relationship("Appointment",back_populates="bill")
    


