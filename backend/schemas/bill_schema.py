import strawberry as sb
from datetime import datetime

from backend.schemas.enums import PaymentStatusEnum


@sb.type
class BillType:

    id: int
    appointment_id: int

    total_amount: float
    payment_status: PaymentStatusEnum

    generated_at: datetime