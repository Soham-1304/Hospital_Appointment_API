from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from backend.models.Appointment import Appointment


def find_by_id(db: Session, id: int) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.id == id).first()


def find_all(db: Session) -> List[Appointment]:
    return db.query(Appointment).all()


def find_by_doctor(db: Session, doctor_id: int) -> List[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )


def find_by_patient(db: Session, patient_id: int) -> List[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .all()
    )


def find_existing_slot(
    db: Session,
    doctor_id: int,
    appointment_date: date,
    time_slot: str
) -> Optional[Appointment]:
    return (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.time_slot == time_slot
        )
        .first()
    )


def save(db: Session, appointment: Appointment) -> Appointment:
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def commit_and_refresh(db: Session, appointment: Appointment) -> Appointment:
    db.commit()
    db.refresh(appointment)
    return appointment


def flush(db: Session, appointment: Appointment) -> Appointment:
    """Flush pending changes without committing — use when coordinating multi-entity saves."""
    db.flush()
    return appointment
