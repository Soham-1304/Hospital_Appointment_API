from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.Patient import Patient


def find_by_id(db: Session, id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == id).first()


def find_by_email(db: Session, email: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.email == email).first()


def find_all(db: Session) -> List[Patient]:
    return db.query(Patient).all()


def save(db: Session, patient: Patient) -> Patient:
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
