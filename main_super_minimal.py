# main_super_minimal.py - Entry point for super minimal deployment
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the super minimal FastAPI app
from backend.main_super_minimal import app

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting SUPER minimal server on {host}:{port}")
    print("🔧 This version has no database, no pydantic, just basic FastAPI")
    uvicorn.run("main_super_minimal:app", host=host, port=port, reload=False, workers=1)