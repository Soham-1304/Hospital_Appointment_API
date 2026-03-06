from typing import Optional
from sqlalchemy.orm import Session

from backend.models.Prescription import Prescription
from backend.models.Enums import AppointmentStatus
import backend.repositories.prescription_repository as prescription_repo
import backend.repositories.appointment_repository as appointment_repo


def get_prescription_by_appointment(
    db: Session,
    appointment_id: int
) -> Optional[Prescription]:
    return prescription_repo.find_by_appointment(db, appointment_id)


def create_prescription(
    db: Session,
    appointment_id: int,
    diagnosis: Optional[str],
    medicines: Optional[str],
    instructions: Optional[str]
) -> Prescription:
    appointment = appointment_repo.find_by_id(db, appointment_id)
    if not appointment:
        raise Exception(f"Appointment with ID {appointment_id} does not exist")

    if appointment.status != AppointmentStatus.COMPLETED:  # type: ignore
        raise Exception("Prescription can only be created for a completed appointment")

    if prescription_repo.find_by_appointment(db, appointment_id):
        raise Exception("A prescription already exists for this appointment")

    prescription = Prescription(
        appointment_id=appointment_id,
        diagnosis=diagnosis,
        medicines=medicines,
        instructions=instructions
    )
    return prescription_repo.save(db, prescription)
