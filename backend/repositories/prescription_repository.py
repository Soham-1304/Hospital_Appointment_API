from typing import Optional
from sqlalchemy.orm import Session

from backend.models.Prescription import Prescription


def find_by_appointment(db: Session, appointment_id: int) -> Optional[Prescription]:
    return (
        db.query(Prescription)
        .filter(Prescription.appointment_id == appointment_id)
        .first()
    )


def save(db: Session, prescription: Prescription) -> Prescription:
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription
