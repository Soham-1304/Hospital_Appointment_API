import strawberry as sb
from datetime import date

@sb.type
class PatientType:
    id:int
    name: str
    email:str
    phone:str
    date_of_birth:date
    gender:str