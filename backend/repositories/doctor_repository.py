from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.Doctor import Doctor


def find_by_id(db: Session, id: int) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.id == id).first()


def find_all(db: Session) -> List[Doctor]:
    return db.query(Doctor).all()


def find_available_by_specialization(db: Session, specialization: str) -> List[Doctor]:
    return (
        db.query(Doctor)
        .filter(
            Doctor.specialization == specialization,
            Doctor.is_available == True
        )
        .all()
    )


def save(db: Session, doctor: Doctor) -> Doctor:
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def commit_and_refresh(db: Session, doctor: Doctor) -> Doctor:
    db.commit()
    db.refresh(doctor)
    return doctor
