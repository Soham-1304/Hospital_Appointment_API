from typing import Optional
from sqlalchemy.orm import Session

from backend.models.Bill import Bill
from backend.models.Enums import PaymentStatus
import backend.repositories.billing_repository as billing_repo


def get_bill_by_appointment(
    db: Session,
    appointment_id: int
) -> Optional[Bill]:
    return billing_repo.find_by_appointment(db, appointment_id)


def update_payment_status(
    db: Session,
    bill_id: int,
    status: PaymentStatus
) -> Bill:
    bill = billing_repo.find_by_id(db, bill_id)

    if not bill:
        raise Exception("Bill not found")

    bill.payment_status = status
    return billing_repo.commit_and_refresh(db, bill)
