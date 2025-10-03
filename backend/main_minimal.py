# backend/main_minimal.py - Minimal version for initial deployment
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from . import database_handler

# Import only basic route modules (comment out heavy ones for now)
from .routes import auth, users, management

# Initialize the database on startup
database_handler.initialize_database()

app = FastAPI(title="Project Netra - Minimal API")

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only lightweight routers first
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(management.router, prefix="/api/management", tags=["General Management"])
app.include_router(users.router, prefix="/api/users", tags=["User Actions"])

# TODO: Add back these routes after basic deployment works:
# app.include_router(principal.router, prefix="/api/principal", tags=["Principal Actions"])
# app.include_router(hod.router, prefix="/api/hod", tags=["HOD Actions"])
# app.include_router(staff.router, prefix="/api/staff", tags=["Staff Actions"])
# app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
# app.include_router(registration.router, prefix="/api/registration", tags=["Registration"])

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "Backend is running - Minimal Version", "version": "1.0"}

@app.get("/health")
def health_check():
    """Health check for Render"""
    return {"status": "healthy", "message": "Project Netra API is operational"}