from typing import List
from datetime import datetime, date
from sqlalchemy.orm import Session

from backend.models.Appointment import Appointment
from backend.models.Bill import Bill
from backend.models.Enums import AppointmentStatus, PaymentStatus

import backend.repositories.appointment_repository as appointment_repo
import backend.repositories.doctor_repository as doctor_repo
import backend.repositories.patient_repository as patient_repo
import backend.repositories.billing_repository as billing_repo


def get_all_appointments(db: Session) -> List[Appointment]:
    return appointment_repo.find_all(db)


def get_appointments_by_doctor(db: Session, doctor_id: int) -> List[Appointment]:
    return appointment_repo.find_by_doctor(db, doctor_id)


def get_appointments_by_patient(db: Session, patient_id: int) -> List[Appointment]:
    return appointment_repo.find_by_patient(db, patient_id)


def create_appointment(
    db: Session,
    patient_id: int,
    doctor_id: int,
    appointment_date: date,
    time_slot: str
) -> Appointment:
    if not doctor_repo.find_by_id(db, doctor_id):
        raise Exception(f"Doctor with ID {doctor_id} does not exist")

    if not patient_repo.find_by_id(db, patient_id):
        raise Exception(f"Patient with ID {patient_id} does not exist")

    existing = appointment_repo.find_existing_slot(db, doctor_id, appointment_date, time_slot)
    if existing:
        raise Exception("Doctor already booked for this time slot")

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        time_slot=time_slot,
        status=AppointmentStatus.SCHEDULED
    )
    return appointment_repo.save(db, appointment)


def complete_appointment(db: Session, appointment_id: int) -> Appointment:
    appointment = appointment_repo.find_by_id(db, appointment_id)
    if not appointment:
        raise Exception("Appointment not found")

    appointment.status = AppointmentStatus.COMPLETED  # type: ignore

    doctor = doctor_repo.find_by_id(db, appointment.doctor_id)
    if not doctor:
        raise Exception("Doctor not found")

    bill = Bill(
        appointment_id=appointment_id,
        total_amount=doctor.consultation_fee,
        payment_status=PaymentStatus.PENDING,
        generated_at=datetime.now()
    )
    # Stage both changes, then commit once so they succeed or fail together
    appointment_repo.flush(db, appointment)
    billing_repo.stage(db, bill)
    return appointment_repo.commit_and_refresh(db, appointment)
