# main_minimal.py - Entry point for minimal deployment
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the minimal FastAPI app
from backend.main_minimal import app

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting minimal server on {host}:{port}")
    uvicorn.run("main_minimal:app", host=host, port=port, reload=False, workers=1)