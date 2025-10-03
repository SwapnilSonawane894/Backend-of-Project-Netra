# main.py - Original structure for Python 3.11
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the FastAPI app
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Project Netra server on {host}:{port}")
    print(f"🐍 Python version: {sys.version}")
    uvicorn.run(app, host=host, port=port, reload=False)