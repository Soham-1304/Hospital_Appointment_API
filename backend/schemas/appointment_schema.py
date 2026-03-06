import strawberry as sb
from datetime import date

from backend.schemas.enums import AppointmentStatusEnum

@sb.type
class AppointmentType:
    id:int
    patient_id:int
    doctor_id:int
    appointment_date:date
    time_slot:str
    status: AppointmentStatusEnum
    notes:str|None
