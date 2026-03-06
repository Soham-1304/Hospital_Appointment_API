import strawberry as sb
from strawberry.types import Info
from typing import Optional
from sqlalchemy.orm import Session
from datetime import date

from backend.models.Enums import PaymentStatus

from backend.schemas.department_schema import DepartmentType
from backend.schemas.patient_schema import PatientType
from backend.schemas.doctor_schema import DoctorType
from backend.schemas.appointment_schema import AppointmentType
from backend.schemas.bill_schema import BillType
from backend.schemas.prescription_schema import PrescriptionType

import backend.services.department_service as department_service
import backend.services.patient_service as patient_service
import backend.services.doctor_service as doctor_service
import backend.services.appointment_service as appointment_service
import backend.services.billing_service as billing_service
import backend.services.prescription_service as prescription_service


@sb.type
class Mutation:


    # ----------------------------
    # Department Mutations
    # ----------------------------

    @sb.field
    def create_department(self, info: Info, name: str, floor_number: Optional[int] = None) -> DepartmentType:
        db: Session = info.context["db"]
        return department_service.create_department(db, name, floor_number)


    # ----------------------------
    # Patient Mutations
    # ----------------------------

    @sb.field
    def create_patient(self, info: Info, name: str, email: str, phone: str, gender: str) -> PatientType:
        db: Session = info.context["db"]
        return patient_service.create_patient(db, name, email, phone, gender)


    # ----------------------------
    # Doctor Mutations
    # ----------------------------

    @sb.field
    def create_doctor(self, info: Info, name: str, specialization: str, consultation_fee: float, department_id: int) -> DoctorType:
        db: Session = info.context["db"]
        return doctor_service.create_doctor(db, name, specialization, consultation_fee, department_id)

    @sb.field
    def set_doctor_availability(self, info: Info, doctor_id: int, is_available: bool) -> DoctorType:
        db: Session = info.context["db"]
        return doctor_service.set_availability(db, doctor_id, is_available)


    # ----------------------------
    # Appointment Mutations
    # ----------------------------

    @sb.field
    def create_appointment(self, info: Info, patient_id: int, doctor_id: int, appointment_date: date, time_slot: str) -> AppointmentType:
        db: Session = info.context["db"]
        return appointment_service.create_appointment(db, patient_id, doctor_id, appointment_date, time_slot)


    # ----------------------------
    # Appointment Status Mutations
    # ----------------------------

    @sb.field
    def complete_appointment(self, info: Info, appointment_id: int) -> AppointmentType:
        db: Session = info.context["db"]
        return appointment_service.complete_appointment(db, appointment_id)


    # ----------------------------
    # Prescription Mutations
    # ----------------------------

    @sb.field
    def create_prescription(
        self,
        info: Info,
        appointment_id: int,
        diagnosis: Optional[str] = None,
        medicines: Optional[str] = None,
        instructions: Optional[str] = None
    ) -> PrescriptionType:
        db: Session = info.context["db"]
        return prescription_service.create_prescription(db, appointment_id, diagnosis, medicines, instructions)


    # ----------------------------
    # Billing Mutations
    # ----------------------------

    @sb.field
    def update_payment_status(self, info: Info, bill_id: int, status: PaymentStatus) -> Optional[BillType]:
        db: Session = info.context["db"]
        return billing_service.update_payment_status(db, bill_id, status)
