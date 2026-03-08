# Hospital Appointment System — GraphQL API

A full-stack hospital appointment management system built with a **GraphQL-first** architecture. The backend exposes a single `/graphql` endpoint for all operations, with a Streamlit frontend for interactive use.

**Live Demo:** [https://hospitalappointment.streamlit.app/](https://hospitalappointment.streamlit.app/)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Strawberry GraphQL |
| Database | PostgreSQL (via SQLAlchemy ORM) |
| Frontend | Streamlit |
| Backend Hosting | Render |
| Frontend Hosting | Streamlit Community Cloud |

---

## Project Structure

```
.
├── backend/
│   ├── main.py                  # FastAPI app entry point, CORS, GraphQL router
│   ├── config.py                # Pydantic settings (env-based config)
│   ├── database.py              # SQLAlchemy engine, session, Base
│   ├── graphql/
│   │   ├── schema.py            # Strawberry schema (Query + Mutation)
│   │   ├── queries.py           # All GraphQL query resolvers
│   │   └── mutations.py         # All GraphQL mutation resolvers
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── Department.py
│   │   ├── Doctor.py
│   │   ├── Patient.py
│   │   ├── Appointment.py
│   │   ├── Prescription.py
│   │   ├── Bill.py
│   │   └── Enums.py             # AppointmentStatus, PaymentStatus enums
│   ├── schemas/                 # Strawberry GraphQL types
│   │   ├── department_schema.py
│   │   ├── doctor_schema.py
│   │   ├── patient_schema.py
│   │   ├── appointment_schema.py
│   │   ├── prescription_schema.py
│   │   └── bill_schema.py
│   ├── repositories/            # DB query layer (data access objects)
│   │   ├── department_repository.py
│   │   ├── doctor_repository.py
│   │   ├── patient_repository.py
│   │   ├── appointment_repository.py
│   │   ├── prescription_repository.py
│   │   └── billing_repository.py
│   └── services/                # Business logic layer
│       ├── department_service.py
│       ├── doctor_service.py
│       ├── patient_service.py
│       ├── appointment_service.py
│       ├── prescription_service.py
│       └── billing_service.py
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
├── requirements.txt             # Backend dependencies
├── render.yaml                  # Render deployment blueprint
└── .env                         # Local environment variables (not committed)
```

---

## Data Models

| Model | Key Fields |
|---|---|
| **Department** | name, floor_number |
| **Doctor** | name, specialization, consultation_fee, is_available, department |
| **Patient** | name, email, phone, gender, date_of_birth |
| **Appointment** | patient, doctor, appointment_date, time_slot, status |
| **Prescription** | appointment, medication details, notes |
| **Bill** | appointment, amount, payment_status |

### Enums

- `AppointmentStatus`: `scheduled` · `completed` · `cancelled` · `no_show`
- `PaymentStatus`: `pending` · `paid` · `failed`

---

## GraphQL API

The entire API is served at a single endpoint: **`POST /graphql`**

An interactive GraphiQL playground is available at `/graphql` in the browser.

### Queries

| Query | Description |
|---|---|
| `departments` | List all departments |
| `department(id)` | Get a department by ID |
| `doctors` | List all doctors |
| `doctor(id)` | Get a doctor by ID |
| `availableDoctors(specialization)` | Filter doctors by specialization & availability |
| `patients` | List all patients |
| `patient(id)` | Get a patient by ID |
| `appointments` | List all appointments |

### Mutations

| Mutation | Description |
|---|---|
| `createDepartment(name, floorNumber)` | Add a new department |
| `createDoctor(name, specialization, consultationFee, departmentId)` | Register a doctor |
| `setDoctorAvailability(doctorId, isAvailable)` | Toggle doctor availability |
| `createPatient(name, email, phone, gender)` | Register a patient |
| `createAppointment(patientId, doctorId, appointmentDate, timeSlot)` | Book an appointment |
| `completeAppointment(appointmentId)` | Mark appointment as completed |

---

## Key Highlights

- **GraphQL-first design** — a single `/graphql` endpoint replaces multiple REST routes. Clients request exactly the fields they need, nothing more.
- **Strawberry + FastAPI** — type-safe GraphQL schema defined entirely in Python using Strawberry's decorator-based approach, mounted onto FastAPI via `GraphQLRouter`.
- **Layered architecture** — clean separation between ORM models → repositories (data access) → services (business logic) → GraphQL resolvers.
- **Conflict prevention** — `UniqueConstraint` on `(doctor_id, appointment_date, time_slot)` enforces no double-booking at the database level.
- **Doctor availability flag** — `is_available` on the Doctor model lets the system filter bookable doctors without touching appointments.
- **Enum-driven status tracking** — appointment lifecycle (`scheduled → completed / cancelled / no_show`) and billing (`pending → paid / failed`) are enforced via database-level enums.
- **PostgreSQL on Render** — provisioned via `render.yaml` blueprint with automatic `DATABASE_URL` injection; supports both PostgreSQL (production) and SQLite (local dev).
- **CORS configured** — backend allows cross-origin requests so the Streamlit frontend can communicate with the API from a different domain.

---

## Running Locally

### 1. Clone & set up environment

```bash
git clone https://github.com/Soham-1304/Hospital_Appointment_API.git
cd Hospital_Appointment_API
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./hospital.db   # or your PostgreSQL connection string
DEBUG=true
```

### 3. Start the backend

```bash
uvicorn backend.main:app --reload
```

GraphiQL playground: [http://localhost:8000/graphql](http://localhost:8000/graphql)

### 4. Start the frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## Deployment

| Component | Platform | Config |
|---|---|---|
| Backend API | [Render](https://render.com) | `render.yaml` (web service + managed PostgreSQL) |
| Frontend | [Streamlit Community Cloud](https://streamlit.io/cloud) | Points to `frontend/app.py` |

The `render.yaml` blueprint provisions the FastAPI web service and a managed PostgreSQL database in one step. The `DATABASE_URL` is automatically injected as an environment variable at runtime.

---

## Dependencies

```
fastapi
uvicorn
strawberry-graphql
sqlalchemy
psycopg2-binary
pydantic
pydantic-settings
python-dotenv
python-dateutil
streamlit
requests
```
