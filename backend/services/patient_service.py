from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.Patient import Patient
import backend.repositories.patient_repository as patient_repo


def get_patient(db: Session, id: int) -> Optional[Patient]:
    return patient_repo.find_by_id(db, id)


def get_all_patients(db: Session) -> List[Patient]:
    return patient_repo.find_all(db)


def create_patient(
    db: Session,
    name: str,
    email: str,
    phone: str,
    gender: str
) -> Patient:
    if patient_repo.find_by_email(db, email):
        raise Exception(f"A patient with email '{email}' already exists")

    patient = Patient(name=name, email=email, phone=phone, gender=gender)
    return patient_repo.save(db, patient)
