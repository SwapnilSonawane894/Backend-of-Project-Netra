# app_standalone.py - Complete Standalone FastAPI app for Render deployment
import os
import sqlite3
import bcrypt
import jwt
from jwt import PyJWTError, ExpiredSignatureError
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Form, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "a-very-bad-default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Database configuration
DB_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
DB_FILE = os.path.join(DB_FOLDER, "project_netra_final.db")
os.makedirs(DB_FOLDER, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="Project Netra - Complete API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Database functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username: str):
    """Get user by username from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def verify_password_original(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash using passlib (original method)"""
    try:
        # Import passlib here to use the same method as original
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token - Original format"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except (PyJWTError, ExpiredSignatureError):
        raise credentials_exception

def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current user from token"""
    return {
        "username": token_data.get("sub"),
        "role": token_data.get("role"),
        "dept": token_data.get("dept"),
        "fullName": token_data.get("fullName"),
        "assignedClass": token_data.get("assignedClass")
    }

# Database query functions
def get_all_students_for_management():
    """Get all students for management"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT roll_no, name, student_class, parent_phone 
            FROM students 
            ORDER BY roll_no
        """)
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    except Exception as e:
        print(f"Database error getting students: {e}")
        return []

def get_timetable_data():
    """Get timetable data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM timetable ORDER BY class_name, day, time_slot")
        timetable = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return timetable
    except Exception as e:
        print(f"Database error getting timetable: {e}")
        return []

# Routes
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "Backend is running - Complete Standalone Version", 
        "version": "2.0",
        "database": "Connected" if os.path.exists(DB_FILE) else "Not Found"
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy", 
        "message": "Project Netra API is operational",
        "database_exists": os.path.exists(DB_FILE),
        "database_path": DB_FILE
    }

# AUTH ROUTES - Using original format with JSON body
class LoginRequest:
    """Simple login request class"""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

@app.post("/api/auth/login")
async def login(request: dict):
    """Login endpoint using JSON body (original format)"""
    username = request.get("username")
    password = request.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=422, detail="Username and password are required")
    
    user = get_user_by_username(username)
    
    if not user or not verify_password_original(password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create JWT token - EXACT same format as original
    token_data = {
        "sub": user["username"], 
        "role": user["role"], 
        "dept": user.get("department"),
        "fullName": user["full_name"],
        "assignedClass": user.get("assigned_class")
    }
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "fullName": user["full_name"],
            "role": user["role"],
            "department": user.get("department"),
            "assignedClass": user.get("assigned_class")
        }
    }

@app.get("/api/auth/test")
async def test_auth():
    """Test endpoint for auth functionality"""
    return {"message": "Auth routes are working", "endpoints": ["/api/auth/login"]}

# MANAGEMENT ROUTES
@app.get("/api/management/students")
async def get_students(current_user: dict = Depends(get_current_user)):
    """Get students based on user role"""
    user_role = current_user.get("role")
    user_dept = current_user.get("dept")
    
    all_students = get_all_students_for_management()
    
    if user_role == 'principal':
        return all_students
    elif user_role in ['hod', 'class_teacher']:
        # Filter by department if needed
        return all_students  # For now return all, can filter later
    else:
        raise HTTPException(status_code=403, detail="Access denied")

@app.get("/api/management/timetable")
async def get_timetable(current_user: dict = Depends(get_current_user)):
    """Get timetable data"""
    try:
        timetable_data = get_timetable_data()
        return {"timetable": timetable_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching timetable: {str(e)}")

# USER ROUTES
@app.get("/api/users/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# ATTENDANCE ROUTES
@app.get("/api/attendance/summary")
async def get_attendance_summary(current_user: dict = Depends(get_current_user)):
    """Get attendance summary - placeholder"""
    return {"message": "Attendance summary endpoint", "user": current_user.get("username")}

# REGISTRATION ROUTES
@app.get("/api/registration/status")
async def get_registration_status(current_user: dict = Depends(get_current_user)):
    """Get registration status - placeholder"""
    return {"message": "Registration status endpoint", "user": current_user.get("username")}

# PRINCIPAL ROUTES
@app.get("/api/principal/dashboard")
async def get_principal_dashboard(current_user: dict = Depends(get_current_user)):
    """Principal dashboard - placeholder"""
    if current_user.get("role") != "principal":
        raise HTTPException(status_code=403, detail="Access denied - Principal only")
    return {"message": "Principal dashboard", "user": current_user.get("username")}

# HOD ROUTES  
@app.get("/api/hod/dashboard")
async def get_hod_dashboard(current_user: dict = Depends(get_current_user)):
    """HOD dashboard - placeholder"""
    if current_user.get("role") != "hod":
        raise HTTPException(status_code=403, detail="Access denied - HOD only")
    return {"message": "HOD dashboard", "user": current_user.get("username")}

# STAFF ROUTES
@app.get("/api/staff/dashboard")
async def get_staff_dashboard(current_user: dict = Depends(get_current_user)):
    """Staff dashboard - placeholder"""
    if current_user.get("role") not in ["staff", "class_teacher"]:
        raise HTTPException(status_code=403, detail="Access denied - Staff only")
    return {"message": "Staff dashboard", "user": current_user.get("username")}

# For direct uvicorn running
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Standalone server on {host}:{port}")
    print(f"📁 Database file: {DB_FILE}")
    print(f"📁 Database exists: {os.path.exists(DB_FILE)}")
    
    uvicorn.run(app, host=host, port=port, reload=False)