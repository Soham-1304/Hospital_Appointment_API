from typing import Optional
from sqlalchemy.orm import Session

from backend.models.Department import Department


def find_by_id(db: Session, id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == id).first()
