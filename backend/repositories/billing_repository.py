from typing import Optional
from sqlalchemy.orm import Session

from backend.models.Bill import Bill


def find_by_id(db: Session, bill_id: int) -> Optional[Bill]:
    return db.query(Bill).filter(Bill.id == bill_id).first()


def find_by_appointment(db: Session, appointment_id: int) -> Optional[Bill]:
    return (
        db.query(Bill)
        .filter(Bill.appointment_id == appointment_id)
        .first()
    )


def save(db: Session, bill: Bill) -> Bill:
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def stage(db: Session, bill: Bill) -> Bill:
    """Add and flush without committing — use when coordinating multi-entity saves."""
    db.add(bill)
    db.flush()
    return bill


def commit_and_refresh(db: Session, bill: Bill) -> Bill:
    db.commit()
    db.refresh(bill)
    return bill
