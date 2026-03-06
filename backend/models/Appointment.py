from sqlalchemy import Column,Integer,String,Date,Enum,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.Enums import AppointmentStatus

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer,primary_key=True,index=True)
    patient_id = Column(Integer,ForeignKey("patients.id"),nullable=False)
    doctor_id = Column(Integer,ForeignKey("doctors.id"),nullable=False)
    appointment_date = Column(Date,nullable=False)
    time_slot = Column(String(20),nullable=False)
    status = Column(Enum(AppointmentStatus),default=AppointmentStatus.SCHEDULED,nullable=False)
    notes = Column(String)

    patient = relationship("Patient",back_populates="appointments")
    doctor = relationship("Doctor",back_populates="appointments")

    prescription = relationship("Prescription",back_populates="appointment",uselist=False)
    bill = relationship("Bill",back_populates="appointment",uselist=False)

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            "time_slot",
            name = "unique_doctor_timeslot"
        ),
    )