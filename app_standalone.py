# app_standalone.py - Standalone FastAPI app for Render deployment
import os
import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "a-very-bad-default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Database configuration
DB_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
DB_FILE = os.path.join(DB_FOLDER, "project_netra_final.db")
os.makedirs(DB_FOLDER, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="Project Netra - Standalone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database functions
def get_user_by_username(username: str):
    """Get user by username from database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
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

# Routes
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "Backend is running - Standalone Version", 
        "version": "1.0",
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

@app.post("/api/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint using Form data"""
    user = get_user_by_username(username)
    
    if not user or not verify_password(password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create JWT token
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
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user.get("department"),
            "assigned_class": user.get("assigned_class")
        }
    }

@app.get("/api/auth/test")
async def test_auth():
    """Test endpoint for auth functionality"""
    return {"message": "Auth routes are working", "endpoints": ["/api/auth/login"]}

# For direct uvicorn running
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Standalone server on {host}:{port}")
    print(f"📁 Database file: {DB_FILE}")
    print(f"📁 Database exists: {os.path.exists(DB_FILE)}")
    
    uvicorn.run(app, host=host, port=port, reload=False)