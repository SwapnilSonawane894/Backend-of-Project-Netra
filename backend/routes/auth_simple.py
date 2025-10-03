# backend/routes/auth_simple.py - Auth without pydantic models
from fastapi import APIRouter, HTTPException, Form
from .. import database_handler
from .. import auth

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint using Form data instead of pydantic models"""
    user = database_handler.get_user_by_username(username)
    
    if not user or not auth.verify_password(password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # The JWT token must now also contain the user's assigned class.
    token_data = {
        "sub": user["username"], 
        "role": user["role"], 
        "dept": user.get("department"),
        "fullName": user["full_name"],
        "assignedClass": user.get("assigned_class") # Add this line
    }
    access_token = auth.create_access_token(data=token_data)
    
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

@router.get("/test")
async def test_auth():
    """Test endpoint for auth functionality"""
    return {"message": "Auth routes are working", "endpoints": ["/login"]}