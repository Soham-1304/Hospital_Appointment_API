import strawberry as sb
from typing import Optional


@sb.type
class PrescriptionType:

    id: int
    appointment_id: int

    diagnosis: Optional[str]
    medicines: Optional[str]
    instructions: Optional[str]