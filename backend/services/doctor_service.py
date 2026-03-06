from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.Doctor import Doctor
import backend.repositories.doctor_repository as doctor_repo
import backend.repositories.department_repository as department_repo


def get_available_doctors(db: Session, specialization: str) -> List[Doctor]:
    return doctor_repo.find_available_by_specialization(db, specialization)


def get_doctor(db: Session, id: int) -> Optional[Doctor]:
    return doctor_repo.find_by_id(db, id)


def get_all_doctors(db: Session) -> List[Doctor]:
    return doctor_repo.find_all(db)


def create_doctor(
    db: Session,
    name: str,
    specialization: str,
    consultation_fee: float,
    department_id: int
) -> Doctor:
    if not department_repo.find_by_id(db, department_id):
        raise Exception(f"Department with ID {department_id} does not exist")

    doctor = Doctor(
        name=name,
        specialization=specialization,
        consultation_fee=consultation_fee,
        department_id=department_id
    )
    return doctor_repo.save(db, doctor)


def set_availability(db: Session, doctor_id: int, is_available: bool) -> Doctor:
    doctor = doctor_repo.find_by_id(db, doctor_id)
    if not doctor:
        raise Exception(f"Doctor with ID {doctor_id} does not exist")
    doctor.is_available = is_available  # type: ignore
    return doctor_repo.commit_and_refresh(db, doctor)
