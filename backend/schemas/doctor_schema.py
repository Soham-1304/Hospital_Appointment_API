import strawberry as sb

@sb.type
class DoctorType:
    id:int
    name: str
    specialization: str
    consultation_fee: float
    is_available: bool