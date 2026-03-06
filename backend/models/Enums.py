import enum

class AppointmentStatus(str,enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class PaymentStatus(str,enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    