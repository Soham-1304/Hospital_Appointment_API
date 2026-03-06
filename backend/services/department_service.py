from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.Department import Department
import backend.repositories.department_repository as department_repo


def get_all_departments(db: Session) -> List[Department]:
    return db.query(Department).all()


def get_department(db: Session, id: int) -> Optional[Department]:
    return department_repo.find_by_id(db, id)


def create_department(db: Session, name: str, floor_number: Optional[int]) -> Department:
    existing = db.query(Department).filter(Department.name == name).first()
    if existing:
        raise Exception(f"Department '{name}' already exists")

    dept = Department(name=name, floor_number=floor_number)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept
