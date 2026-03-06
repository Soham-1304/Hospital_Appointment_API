import strawberry as sb
from typing import Optional


@sb.type
class DepartmentType:
    id: int
    name: str
    floor_number: Optional[int]
