import strawberry
from strawberry.types import Info
from typing import Sequence, Optional
from sqlalchemy.orm import Session

from backend.schemas.department_schema import DepartmentType
from backend.schemas.doctor_schema import DoctorType
from backend.schemas.patient_schema import PatientType
from backend.schemas.appointment_schema import AppointmentType
from backend.schemas.prescription_schema import PrescriptionType
from backend.schemas.bill_schema import BillType

import backend.services.department_service as department_service
import backend.services.doctor_service as doctor_service
import backend.services.patient_service as patient_service
import backend.services.appointment_service as appointment_service
import backend.services.prescription_service as prescription_service
import backend.services.billing_service as billing_service


@strawberry.type
class Query:


    # ----------------------------
    # Department Queries
    # ----------------------------

    @strawberry.field
    def departments(self, info: Info) -> Sequence[DepartmentType]:
        db: Session = info.context["db"]
        return department_service.get_all_departments(db)


    @strawberry.field
    def department(self, info: Info, id: int) -> Optional[DepartmentType]:
        db: Session = info.context["db"]
        return department_service.get_department(db, id)


    # ----------------------------
    # Doctor Queries
    # ----------------------------

    @strawberry.field
    def available_doctors(
        self,
        info: Info,
        specialization: str
    ) -> Sequence[DoctorType]:
        db: Session = info.context["db"]
        return doctor_service.get_available_doctors(db, specialization)


    @strawberry.field
    def doctor(
        self,
        info: Info,
        id: int
    ) -> Optional[DoctorType]:
        db: Session = info.context["db"]
        return doctor_service.get_doctor(db, id)


    @strawberry.field
    def doctors(self, info: Info) -> Sequence[DoctorType]:
        db: Session = info.context["db"]
        return doctor_service.get_all_doctors(db)


    # ----------------------------
    # Patient Queries
    # ----------------------------

    @strawberry.field
    def patient(
        self,
        info: Info,
        id: int
    ) -> Optional[PatientType]:
        db: Session = info.context["db"]
        return patient_service.get_patient(db, id)


    @strawberry.field
    def patients(self, info: Info) -> Sequence[PatientType]:
        db: Session = info.context["db"]
        return patient_service.get_all_patients(db)


    # ----------------------------
    # Appointment Queries
    # ----------------------------

    @strawberry.field
    def appointments(self, info: Info) -> Sequence[AppointmentType]:
        db: Session = info.context["db"]
        return appointment_service.get_all_appointments(db)


    @strawberry.field
    def appointments_by_doctor(
        self,
        info: Info,
        doctor_id: int
    ) -> Sequence[AppointmentType]:
        db: Session = info.context["db"]
        return appointment_service.get_appointments_by_doctor(db, doctor_id)


    @strawberry.field
    def appointments_by_patient(
        self,
        info: Info,
        patient_id: int
    ) -> Sequence[AppointmentType]:
        db: Session = info.context["db"]
        return appointment_service.get_appointments_by_patient(db, patient_id)


    # ----------------------------
    # Prescription Queries
    # ----------------------------

    @strawberry.field
    def prescription_by_appointment(
        self,
        info: Info,
        appointment_id: int
    ) -> Optional[PrescriptionType]:
        db: Session = info.context["db"]
        return prescription_service.get_prescription_by_appointment(db, appointment_id)


    # ----------------------------
    # Billing Queries
    # ----------------------------

    @strawberry.field
    def bill_by_appointment(
        self,
        info: Info,
        appointment_id: int
    ) -> Optional[BillType]:
        db: Session = info.context["db"]
        return billing_service.get_bill_by_appointment(db, appointment_id)