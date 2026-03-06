import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load root .env when running locally (no-op in production)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Priority: Streamlit secret (production) → env var → localhost default
_host = os.getenv("BACKEND_HOST", "127.0.0.1")
_port = os.getenv("BACKEND_PORT", "8000")
_default_url = f"http://{_host}:{_port}/graphql"
GRAPHQL_URL = st.secrets.get("GRAPHQL_URL", _default_url)

st.set_page_config(page_title="Hospital Management", layout="wide", page_icon="🏥")

st.title("🏥 Hospital Appointment Management")
st.caption("Setup order: **1 → Departments** → **2 → Doctors** → **3 → Patients** → **4 → Book Appointment** → **5 → Complete Appointment** → **6 → Prescription** → **7 → Billing**")

# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def gql(query: str):
    try:
        resp = requests.post(GRAPHQL_URL, json={"query": query}, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to server at {GRAPHQL_URL}. Is it running?"}
    except Exception as e:
        return {"error": str(e)}


def show_result(result: dict):
    if "error" in result:
        st.error(result["error"])
        return None
    if "errors" in result:
        for e in result["errors"]:
            st.error(f"GraphQL Error: {e['message']}")
        return None
    return result.get("data", {})


# ---------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------

tabs = st.tabs([
    "🏢 Departments",
    "👨‍⚕️ Doctors",
    "🧑 Patients",
    "📅 Appointments",
    "💊 Prescriptions",
    "💳 Billing",
    "🔧 Raw Query",
])


# ===============================================================
# TAB 0 — DEPARTMENTS
# ===============================================================
with tabs[0]:
    st.subheader("Departments")
    st.info("Create departments first — doctors are assigned to a department.")
    sub = st.radio("Action", ["All Departments", "Add Department"], horizontal=True)

    if sub == "All Departments":
        if st.button("Load Departments"):
            data = show_result(gql("{ departments { id name floorNumber } }"))
            if data and data.get("departments"):
                st.dataframe(data["departments"], use_container_width=True)
            elif data is not None:
                st.info("No departments yet. Add one first.")

    elif sub == "Add Department":
        with st.form("add_dept"):
            name = st.text_input("Department Name", placeholder="e.g. Cardiology")
            floor = st.number_input("Floor Number (optional)", min_value=0, step=1, value=0)
            if st.form_submit_button("Create Department"):
                floor_val = floor if floor > 0 else "null"
                q = f"""
                mutation {{
                  createDepartment(name: "{name}", floorNumber: {floor_val}) {{
                    id name floorNumber
                  }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("createDepartment"):
                    d = data["createDepartment"]
                    st.success(f"Department created — ID: {d['id']} | {d['name']} (Floor {d['floorNumber']})")


# ===============================================================
# TAB 1 — DOCTORS
# ===============================================================
with tabs[1]:
    st.subheader("Doctors")
    st.info("Requires a valid Department ID. Create departments first.")
    sub = st.radio("Action", ["All Doctors", "Find by ID", "Available by Specialization", "Add Doctor", "Toggle Availability"], horizontal=True)

    if sub == "All Doctors":
        if st.button("Load Doctors"):
            data = show_result(gql("{ doctors { id name specialization consultationFee isAvailable } }"))
            if data and data.get("doctors"):
                st.dataframe(data["doctors"], use_container_width=True)
            elif data is not None:
                st.info("No doctors found.")

    elif sub == "Find by ID":
        with st.form("doctor_by_id"):
            doc_id = st.number_input("Doctor ID", min_value=1, step=1)
            if st.form_submit_button("Search"):
                data = show_result(gql(f"{{ doctor(id: {doc_id}) {{ id name specialization consultationFee isAvailable }} }}"))
                if data:
                    d = data.get("doctor")
                    if d:
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Name", d["name"])
                        c2.metric("Specialization", d["specialization"])
                        c3.metric("Fee", f"${d['consultationFee']}")
                        st.success("Available" if d["isAvailable"] else "Not Available")
                    else:
                        st.warning("Doctor not found.")

    elif sub == "Available by Specialization":
        with st.form("avail_doctors"):
            spec = st.text_input("Specialization", placeholder="e.g. Cardiology")
            if st.form_submit_button("Search"):
                data = show_result(gql(f'{{ availableDoctors(specialization: "{spec}") {{ id name consultationFee }} }}'))
                if data and data.get("availableDoctors"):
                    st.dataframe(data["availableDoctors"], use_container_width=True)
                elif data is not None:
                    st.info("No available doctors for that specialization.")

    elif sub == "Add Doctor":
        with st.form("add_doctor"):
            name = st.text_input("Name")
            spec = st.text_input("Specialization")
            fee = st.number_input("Consultation Fee", min_value=0.0, step=0.5)
            dept_id = st.number_input("Department ID", min_value=1, step=1,
                                      help="Must be an existing department ID. Check the Departments tab.")
            if st.form_submit_button("Create Doctor"):
                q = f"""
                mutation {{
                  createDoctor(
                    name: "{name}"
                    specialization: "{spec}"
                    consultationFee: {fee}
                    departmentId: {dept_id}
                  ) {{ id name specialization }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("createDoctor"):
                    d = data["createDoctor"]
                    st.success(f"Doctor created — ID: {d['id']} | {d['name']} ({d['specialization']})")

    elif sub == "Toggle Availability":
        with st.form("toggle_avail"):
            doc_id = st.number_input("Doctor ID", min_value=1, step=1)
            is_avail = st.radio("Set Availability", ["Available", "Not Available"], horizontal=True)
            if st.form_submit_button("Update"):
                avail_bool = "true" if is_avail == "Available" else "false"
                q = f"""
                mutation {{
                  setDoctorAvailability(doctorId: {doc_id}, isAvailable: {avail_bool}) {{
                    id name isAvailable
                  }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("setDoctorAvailability"):
                    d = data["setDoctorAvailability"]
                    status_label = "Available ✅" if d["isAvailable"] else "Not Available ❌"
                    st.success(f"Dr. {d['name']} (ID {d['id']}) → {status_label}")


# ===============================================================
# TAB 2 — PATIENTS
# ===============================================================
with tabs[2]:
    st.subheader("Patients")
    sub = st.radio("Action", ["All Patients", "Find by ID", "Add Patient"], horizontal=True)

    if sub == "All Patients":
        if st.button("Load Patients"):
            data = show_result(gql("{ patients { id name email phone gender } }"))
            if data and data.get("patients"):
                st.dataframe(data["patients"], use_container_width=True)
            elif data is not None:
                st.info("No patients found.")

    elif sub == "Find by ID":
        with st.form("patient_by_id"):
            pid = st.number_input("Patient ID", min_value=1, step=1)
            if st.form_submit_button("Search"):
                data = show_result(gql(f"{{ patient(id: {pid}) {{ id name email phone gender }} }}"))
                if data:
                    p = data.get("patient")
                    if p:
                        c1, c2 = st.columns(2)
                        c1.metric("Name", p["name"])
                        c2.metric("Gender", p["gender"] or "—")
                        st.write(f"**Email:** {p['email']}  |  **Phone:** {p['phone'] or '—'}")
                    else:
                        st.warning("Patient not found.")

    elif sub == "Add Patient":
        with st.form("add_patient"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            if st.form_submit_button("Register Patient"):
                q = f"""
                mutation {{
                  createPatient(
                    name: "{name}"
                    email: "{email}"
                    phone: "{phone}"
                    gender: "{gender}"
                  ) {{ id name email }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("createPatient"):
                    p = data["createPatient"]
                    st.success(f"Patient registered — ID: {p['id']} | {p['name']} ({p['email']})")


# ===============================================================
# TAB 3 — APPOINTMENTS
# ===============================================================
with tabs[3]:
    st.subheader("Appointments")
    st.info("Requires valid Patient ID and Doctor ID.")
    sub = st.radio("Action", ["All", "By Doctor", "By Patient", "Book", "Complete"], horizontal=True)

    if sub == "All":
        if st.button("Load All Appointments"):
            data = show_result(gql("{ appointments { id patientId doctorId appointmentDate timeSlot status } }"))
            if data and data.get("appointments"):
                st.dataframe(data["appointments"], use_container_width=True)
            elif data is not None:
                st.info("No appointments found.")

    elif sub == "By Doctor":
        with st.form("appt_by_doc"):
            doc_id = st.number_input("Doctor ID", min_value=1, step=1)
            if st.form_submit_button("Search"):
                data = show_result(gql(f"{{ appointmentsByDoctor(doctorId: {doc_id}) {{ id patientId appointmentDate timeSlot status }} }}"))
                if data and data.get("appointmentsByDoctor"):
                    st.dataframe(data["appointmentsByDoctor"], use_container_width=True)
                elif data is not None:
                    st.info("No appointments for this doctor.")

    elif sub == "By Patient":
        with st.form("appt_by_pat"):
            pat_id = st.number_input("Patient ID", min_value=1, step=1)
            if st.form_submit_button("Search"):
                data = show_result(gql(f"{{ appointmentsByPatient(patientId: {pat_id}) {{ id doctorId appointmentDate timeSlot status }} }}"))
                if data and data.get("appointmentsByPatient"):
                    st.dataframe(data["appointmentsByPatient"], use_container_width=True)
                elif data is not None:
                    st.info("No appointments for this patient.")

    elif sub == "Book":
        with st.form("book_appt"):
            c1, c2 = st.columns(2)
            pat_id = c1.number_input("Patient ID", min_value=1, step=1)
            doc_id = c2.number_input("Doctor ID", min_value=1, step=1)
            appt_date = st.date_input("Appointment Date")
            time_slot = st.text_input("Time Slot", placeholder="e.g. 10:00 AM")
            if st.form_submit_button("Book Appointment"):
                q = f"""
                mutation {{
                  createAppointment(
                    patientId: {pat_id}
                    doctorId: {doc_id}
                    appointmentDate: "{appt_date}"
                    timeSlot: "{time_slot}"
                  ) {{ id status appointmentDate timeSlot }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("createAppointment"):
                    a = data["createAppointment"]
                    st.success(f"Booked — ID: {a['id']} | {a['appointmentDate']} {a['timeSlot']} | {a['status']}")

    elif sub == "Complete":
        with st.form("complete_appt"):
            appt_id = st.number_input("Appointment ID", min_value=1, step=1)
            if st.form_submit_button("Mark as Completed"):
                q = f"""
                mutation {{
                  completeAppointment(appointmentId: {appt_id}) {{
                    id status
                  }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("completeAppointment"):
                    a = data["completeAppointment"]
                    st.success(f"Appointment {a['id']} → {a['status']}. Bill generated automatically.")
                    st.session_state["pending_rx_appt"] = int(appt_id)

        if "pending_rx_appt" in st.session_state:
            cid = st.session_state["pending_rx_appt"]
            st.divider()
            st.markdown(f"#### 💊 Write Prescription for Appointment #{cid}")
            st.caption("The appointment is completed. Add a prescription now or skip.")
            with st.form("write_rx"):
                diagnosis = st.text_area("Diagnosis", placeholder="e.g. Hypertension Stage 1")
                medicines = st.text_area("Medicines", placeholder="e.g. Amlodipine 5mg, Aspirin 75mg")
                instructions = st.text_area("Instructions / Dosage Notes", placeholder="e.g. Take after meals, avoid alcohol")
                c1, c2 = st.columns(2)
                skip_rx = c1.form_submit_button("⏭ Skip")
                save_rx = c2.form_submit_button("✅ Create Prescription")
                if skip_rx:
                    st.session_state.pop("pending_rx_appt", None)
                if save_rx:
                    diag_esc = diagnosis.replace('"', '\\"')
                    meds_esc = medicines.replace('"', '\\"')
                    instr_esc = instructions.replace('"', '\\"')
                    q2 = f'''
                    mutation {{
                      createPrescription(
                        appointmentId: {cid}
                        diagnosis: "{diag_esc}"
                        medicines: "{meds_esc}"
                        instructions: "{instr_esc}"
                      ) {{ id appointmentId diagnosis }}
                    }}
                    '''
                    pdata = show_result(gql(q2))
                    if pdata and pdata.get("createPrescription"):
                        p = pdata["createPrescription"]
                        st.success(f"Prescription #{p['id']} saved for Appointment #{p['appointmentId']}")
                        st.session_state.pop("pending_rx_appt", None)


# ===============================================================
# TAB 4 — PRESCRIPTIONS
# ===============================================================
with tabs[4]:
    st.subheader("Prescriptions")
    sub = st.radio("Action", ["View by Appointment", "Create Prescription"], horizontal=True, key="rx_sub")

    if sub == "View by Appointment":
        with st.form("prescription"):
            appt_id = st.number_input("Appointment ID", min_value=1, step=1)
            if st.form_submit_button("Fetch Prescription"):
                data = show_result(gql(f"{{ prescriptionByAppointment(appointmentId: {appt_id}) {{ id diagnosis medicines instructions }} }}"))
                if data:
                    p = data.get("prescriptionByAppointment")
                    if p:
                        st.markdown(f"**Diagnosis:** {p['diagnosis'] or '—'}")
                        st.markdown(f"**Medicines:** {p['medicines'] or '—'}")
                        st.markdown(f"**Instructions:** {p['instructions'] or '—'}")
                    else:
                        st.info("No prescription found for this appointment.")

    elif sub == "Create Prescription":
        st.info("The appointment must be marked as **Completed** before adding a prescription.")
        with st.form("create_rx"):
            appt_id = st.number_input("Appointment ID", min_value=1, step=1)
            diagnosis = st.text_area("Diagnosis", placeholder="e.g. Hypertension Stage 1")
            medicines = st.text_area("Medicines", placeholder="e.g. Amlodipine 5mg, Aspirin 75mg")
            instructions = st.text_area("Instructions / Dosage Notes", placeholder="e.g. Take after meals")
            if st.form_submit_button("Create Prescription"):
                diag_esc = diagnosis.replace('"', '\\"')
                meds_esc = medicines.replace('"', '\\"')
                instr_esc = instructions.replace('"', '\\"')
                q = f'''
                mutation {{
                  createPrescription(
                    appointmentId: {appt_id}
                    diagnosis: "{diag_esc}"
                    medicines: "{meds_esc}"
                    instructions: "{instr_esc}"
                  ) {{ id appointmentId diagnosis }}
                }}
                '''
                data = show_result(gql(q))
                if data and data.get("createPrescription"):
                    p = data["createPrescription"]
                    st.success(f"Prescription #{p['id']} created for Appointment #{p['appointmentId']}")
                    st.markdown(f"**Diagnosis recorded:** {p['diagnosis'] or '—'}")


# ===============================================================
# TAB 5 — BILLING
# ===============================================================
with tabs[5]:
    st.subheader("Billing")
    sub = st.radio("Action", ["View Bill", "Update Payment Status"], horizontal=True)

    if sub == "View Bill":
        with st.form("view_bill"):
            appt_id = st.number_input("Appointment ID", min_value=1, step=1)
            if st.form_submit_button("Fetch Bill"):
                data = show_result(gql(f"{{ billByAppointment(appointmentId: {appt_id}) {{ id totalAmount paymentStatus generatedAt }} }}"))
                if data:
                    b = data.get("billByAppointment")
                    if b:
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Bill ID", b["id"])
                        c2.metric("Total Amount", f"${b['totalAmount']}")
                        c3.metric("Status", b["paymentStatus"])
                        st.caption(f"Generated at: {b['generatedAt']}")
                    else:
                        st.info("No bill found. Complete the appointment first.")

    elif sub == "Update Payment Status":
        with st.form("update_bill"):
            bill_id = st.number_input("Bill ID", min_value=1, step=1)
            status = st.selectbox("New Status", ["paid", "pending", "failed"])
            if st.form_submit_button("Update Status"):
                q = f"""
                mutation {{
                  updatePaymentStatus(billId: {bill_id}, status: {status.upper()}) {{
                    id paymentStatus totalAmount
                  }}
                }}
                """
                data = show_result(gql(q))
                if data and data.get("updatePaymentStatus"):
                    b = data["updatePaymentStatus"]
                    st.success(f"Bill {b['id']} → {b['paymentStatus']} | ${b['totalAmount']}")


# ===============================================================
# TAB 6 — RAW QUERY
# ===============================================================
with tabs[6]:
    st.subheader("Raw GraphQL Query")
    query_text = st.text_area("Query / Mutation", height=250, placeholder="{ doctors { id name } }")
    if st.button("Run"):
        if query_text.strip():
            result = gql(query_text)
            if "errors" in result:
                for e in result["errors"]:
                    st.error(e["message"])
            elif "error" in result:
                st.error(result["error"])
            else:
                st.json(result.get("data", result))
        else:
            st.warning("Enter a query first.")

            st.warning("Enter a query first.")