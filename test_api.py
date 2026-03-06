"""
End-to-end API test script for the Hospital Appointment System.
Run with: python test_api.py
Server must be running on http://127.0.0.1:8000
"""

import requests
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()  # reads root .env

_host = os.getenv("BACKEND_HOST", "127.0.0.1")
_port = os.getenv("BACKEND_PORT", "8000")
URL = f"http://{_host}:{_port}/graphql"
PASS = "\033[92m PASS\033[0m"
FAIL = "\033[91m FAIL\033[0m"

results = []

# Unique suffix so each test run doesn't collide with previous data
RUN = str(int(time.time()))[-5:]  # last 5 digits of epoch, e.g. "84201"


def gql(query: str, label: str):
    try:
        resp = requests.post(URL, json={"query": query}, timeout=5)
        resp.raise_for_status()
        body = resp.json()
    except Exception as e:
        print(f"[{FAIL}] {label}: {e}")
        results.append((label, False))
        return None

    if "errors" in body:
        msg = body["errors"][0]["message"]
        print(f"[{FAIL}] {label}: {msg}")
        results.append((label, False))
        return None

    data = body.get("data", {})
    print(f"[{PASS}] {label}")
    results.append((label, True))
    return data


def gql_expect_error(query: str, label: str):
    """Passes when the server returns a GraphQL error (validation rejection test)."""
    try:
        resp = requests.post(URL, json={"query": query}, timeout=5)
        resp.raise_for_status()
        body = resp.json()
    except Exception as e:
        print(f"[{FAIL}] {label}: connection error — {e}")
        results.append((label, False))
        return

    if "errors" in body:
        msg = body["errors"][0]["message"]
        print(f"[{PASS}] {label}: correctly rejected → {msg}")
        results.append((label, True))
    else:
        print(f"[{FAIL}] {label}: expected rejection but server accepted the request")
        results.append((label, False))


# ---------------------------------------------------------------
# Track created IDs
# ---------------------------------------------------------------
dept_id = None
doctor_id = None
patient_id = None
appointment_id = None
bill_id = None


# ---------------------------------------------------------------
# 1. Create Department
# ---------------------------------------------------------------
data = gql(f"""
mutation {{
  createDepartment(name: "Cardiology_{RUN}", floorNumber: 2) {{
    id name floorNumber
  }}
}}
""", "Create Department")
if data:
    dept_id = data["createDepartment"]["id"]
    print(f"       → Department ID: {dept_id}")


# ---------------------------------------------------------------
# 2. List Departments
# ---------------------------------------------------------------
gql("{ departments { id name floorNumber } }", "List Departments")


# ---------------------------------------------------------------
# 3. Create Doctor (requires dept_id)
# ---------------------------------------------------------------
if dept_id:
    data = gql(f"""
    mutation {{
      createDoctor(
        name: "Dr. Alice_{RUN}"
        specialization: "Cardiology_{RUN}"
        consultationFee: 500.0
        departmentId: {dept_id}
      ) {{ id name specialization }}
    }}
    """, "Create Doctor")
    if data:
        doctor_id = data["createDoctor"]["id"]
        print(f"       → Doctor ID: {doctor_id}")
else:
    print(f"[SKIP] Create Doctor — no department")


# ---------------------------------------------------------------
# 4. List Doctors
# ---------------------------------------------------------------
gql("{ doctors { id name specialization consultationFee isAvailable } }", "List Doctors")


# ---------------------------------------------------------------
# 5. Get Doctor by ID
# ---------------------------------------------------------------
if doctor_id:
    gql(f"{{ doctor(id: {doctor_id}) {{ id name specialization }} }}", "Get Doctor by ID")


# ---------------------------------------------------------------
# 6. Available Doctors by Specialization
# ---------------------------------------------------------------
gql(f'{{ availableDoctors(specialization: "Cardiology_{RUN}") {{ id name }} }}', "Available Doctors by Specialization")


# ---------------------------------------------------------------
# 7. Create Patient
# ---------------------------------------------------------------
data = gql(f"""
mutation {{
  createPatient(
    name: "John Doe"
    email: "john_{RUN}@example.com"
    phone: "9876543210"
    gender: "Male"
  ) {{ id name email }}
}}
""", "Create Patient")
if data:
    patient_id = data["createPatient"]["id"]
    print(f"       → Patient ID: {patient_id}")


# ---------------------------------------------------------------
# 8. Duplicate email check
# ---------------------------------------------------------------
gql_expect_error(f"""
mutation {{
  createPatient(
    name: "John Duplicate"
    email: "john_{RUN}@example.com"
    phone: "0000000000"
    gender: "Male"
  ) {{ id }}
}}
""", "Duplicate Email Rejected")


# ---------------------------------------------------------------
# 9. List Patients
# ---------------------------------------------------------------
gql("{ patients { id name email phone gender } }", "List Patients")


# ---------------------------------------------------------------
# 10. Get Patient by ID
# ---------------------------------------------------------------
if patient_id:
    gql(f"{{ patient(id: {patient_id}) {{ id name email }} }}", "Get Patient by ID")


# ---------------------------------------------------------------
# 11. Book Appointment (requires doctor_id + patient_id)
# ---------------------------------------------------------------
if doctor_id and patient_id:
    data = gql(f"""
    mutation {{
      createAppointment(
        patientId: {patient_id}
        doctorId: {doctor_id}
        appointmentDate: "2026-04-01"
        timeSlot: "10:00 AM"
      ) {{ id status appointmentDate timeSlot }}
    }}
    """, "Book Appointment")
    if data:
        appointment_id = data["createAppointment"]["id"]
        print(f"       → Appointment ID: {appointment_id}")
else:
    print("[SKIP] Book Appointment — missing doctor or patient")


# ---------------------------------------------------------------
# 12. Duplicate slot check
# ---------------------------------------------------------------
if doctor_id and patient_id:
    gql_expect_error(f"""
    mutation {{
      createAppointment(
        patientId: {patient_id}
        doctorId: {doctor_id}
        appointmentDate: "2026-04-01"
        timeSlot: "10:00 AM"
      ) {{ id }}
    }}
    """, "Duplicate Slot Rejected")


# ---------------------------------------------------------------
# 13. Invalid Doctor ID check
# ---------------------------------------------------------------
if patient_id:
    gql_expect_error(f"""
    mutation {{
      createAppointment(
        patientId: {patient_id}
        doctorId: 9999
        appointmentDate: "2026-04-02"
        timeSlot: "11:00 AM"
      ) {{ id }}
    }}
    """, "Invalid Doctor ID Rejected")


# ---------------------------------------------------------------
# 14. List All Appointments
# ---------------------------------------------------------------
gql("{ appointments { id patientId doctorId appointmentDate timeSlot status } }", "List All Appointments")


# ---------------------------------------------------------------
# 15. Appointments by Doctor
# ---------------------------------------------------------------
if doctor_id:
    gql(f"{{ appointmentsByDoctor(doctorId: {doctor_id}) {{ id status }} }}", "Appointments by Doctor")


# ---------------------------------------------------------------
# 16. Appointments by Patient
# ---------------------------------------------------------------
if patient_id:
    gql(f"{{ appointmentsByPatient(patientId: {patient_id}) {{ id status }} }}", "Appointments by Patient")


# ---------------------------------------------------------------
# 17. Complete Appointment (generates bill)
# ---------------------------------------------------------------
if appointment_id:
    gql(f"""
    mutation {{
      completeAppointment(appointmentId: {appointment_id}) {{
        id status
      }}
    }}
    """, "Complete Appointment")


# ---------------------------------------------------------------
# 18. Get Bill by Appointment
# ---------------------------------------------------------------
if appointment_id:
    data = gql(f"""
    {{
      billByAppointment(appointmentId: {appointment_id}) {{
        id totalAmount paymentStatus generatedAt
      }}
    }}
    """, "Get Bill by Appointment")
    if data and data.get("billByAppointment"):
        bill_id = data["billByAppointment"]["id"]
        print(f"       → Bill ID: {bill_id}, Amount: ${data['billByAppointment']['totalAmount']}")


# ---------------------------------------------------------------
# 19. Update Payment Status
# ---------------------------------------------------------------
if bill_id:
    gql(f"""
    mutation {{
      updatePaymentStatus(billId: {bill_id}, status: PAID) {{
        id paymentStatus
      }}
    }}
    """, "Update Payment Status to PAID")


prescription_id = None

# ---------------------------------------------------------------
# 20. Create Prescription (appointment must be COMPLETED)
# ---------------------------------------------------------------
if appointment_id:
    data = gql(f"""
    mutation {{
      createPrescription(
        appointmentId: {appointment_id}
        diagnosis: "Hypertension Stage 1"
        medicines: "Amlodipine 5mg, Aspirin 75mg"
        instructions: "Take after meals. No alcohol."
      ) {{ id appointmentId diagnosis }}
    }}
    """, "Create Prescription")
    if data and data.get("createPrescription"):
        prescription_id = data["createPrescription"]["id"]
        print(f"       → Prescription ID: {prescription_id}")


# ---------------------------------------------------------------
# 21. Get Prescription by Appointment
# ---------------------------------------------------------------
if appointment_id:
    gql(f"""
    {{
      prescriptionByAppointment(appointmentId: {appointment_id}) {{
        id diagnosis medicines instructions
      }}
    }}
    """, "Get Prescription by Appointment")


# ---------------------------------------------------------------
# 22. Duplicate Prescription Rejected
# ---------------------------------------------------------------
if appointment_id:
    gql_expect_error(f"""
    mutation {{
      createPrescription(
        appointmentId: {appointment_id}
        diagnosis: "Duplicate attempt"
      ) {{ id }}
    }}
    """, "Duplicate Prescription Rejected")


# ---------------------------------------------------------------
# 23. Prescription on SCHEDULED appointment rejected
# ---------------------------------------------------------------
if doctor_id and patient_id:
    data2 = gql(f"""
    mutation {{
      createAppointment(
        patientId: {patient_id}
        doctorId: {doctor_id}
        appointmentDate: "2026-05-01"
        timeSlot: "02:00 PM"
      ) {{ id status }}
    }}
    """, "Book Second Appointment (for validation test)")
    second_appt_id = data2["createAppointment"]["id"] if data2 and data2.get("createAppointment") else None

    if second_appt_id:
        gql_expect_error(f"""
        mutation {{
          createPrescription(
            appointmentId: {second_appt_id}
            diagnosis: "Should fail — not completed"
          ) {{ id }}
        }}
        """, "Prescription on SCHEDULED Appointment Rejected")


# ---------------------------------------------------------------
# 24. Set Doctor Availability to False
# ---------------------------------------------------------------
if doctor_id:
    gql(f"""
    mutation {{
      setDoctorAvailability(doctorId: {doctor_id}, isAvailable: false) {{
        id name isAvailable
      }}
    }}
    """, "Set Doctor Availability → False")


# ---------------------------------------------------------------
# 25. Set Doctor Availability back to True
# ---------------------------------------------------------------
if doctor_id:
    data = gql(f"""
    mutation {{
      setDoctorAvailability(doctorId: {doctor_id}, isAvailable: true) {{
        id name isAvailable
      }}
    }}
    """, "Set Doctor Availability → True")
    if data and data.get("setDoctorAvailability"):
        d = data["setDoctorAvailability"]
        if not d["isAvailable"]:
            print(f"       ⚠  Expected isAvailable=true but got false")
            results[-1] = (results[-1][0], False)


# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
print("\n" + "=" * 50)
passed = sum(1 for _, ok in results if ok)
failed = sum(1 for _, ok in results if not ok)
print(f"  Results: {passed} passed, {failed} failed out of {len(results)} tests")
if failed:
    print("\n  Failed tests:")
    for name, ok in results:
        if not ok:
            print(f"    - {name}")
print("=" * 50)
sys.exit(0 if failed == 0 else 1)
