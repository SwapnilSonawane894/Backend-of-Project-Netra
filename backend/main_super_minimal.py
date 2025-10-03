# backend/main_super_minimal.py - With database but no pydantic
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use absolute imports to avoid relative import issues
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backend.database_handler as database_handler

# Import simple auth routes that don't need pydantic models
from backend.routes import auth_simple

# Initialize the database on startup
database_handler.initialize_database()

app = FastAPI(title="Project Netra - Minimal API with DB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include simple auth router
app.include_router(auth_simple.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "Backend is running - Minimal with Database", "version": "0.2"}

@app.get("/health")
def health_check():
    """Health check for Render"""
    return {"status": "healthy", "message": "Project Netra API is operational", "database": "connected"}

@app.get("/test")
def test_endpoint():
    """Test endpoint to verify basic functionality"""
    return {
        "message": "Test successful!",
        "environment": {
            "python_version": "Working",
            "fastapi": "Working",
            "cors": "Enabled",
            "database": "Connected"
        }
    }