from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import Base, engine, get_db

# Import models so SQLAlchemy registers them
from backend.models.Department import Department
from backend.models.Doctor import Doctor
from backend.models.Patient import Patient
from backend.models.Appointment import Appointment
from backend.models.Prescription import Prescription
from backend.models.Bill import Bill

from backend.graphql.schema import schema


# Create DB tables
Base.metadata.create_all(bind=engine)


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


# GraphQL context (inject DB session)
async def get_context(db: Session = Depends(get_db)):
    return {"db": db}


# GraphQL router
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)


# Mount GraphQL endpoint
app.include_router(graphql_app, prefix=settings.api_prefix)


# Simple health check route
@app.get("/")
def root():
    return {"message": "Hospital Appointment API running"}