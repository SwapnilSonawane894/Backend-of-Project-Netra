# main_super_minimal.py - Entry point for super minimal deployment
import os
import sys

# Add the current directory and backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'backend'))

# Import the super minimal FastAPI app directly
from backend.main_super_minimal import app

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting SUPER minimal server on {host}:{port}")
    print("🔧 This version includes database and auth support")
    uvicorn.run(app, host=host, port=port, reload=False)