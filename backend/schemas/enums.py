import strawberry as sb
from backend.models.Enums import AppointmentStatus,PaymentStatus

AppointmentStatusEnum = sb.enum(AppointmentStatus)
PaymentStatusEnum = sb.enum(PaymentStatus)