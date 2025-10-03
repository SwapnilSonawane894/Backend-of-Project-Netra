#!/usr/bin/env python3
"""
Test script to verify the application works before deployment
Run this locally to catch any issues before pushing to Render
"""

import sys
import os
import subprocess

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import fastapi
        import uvicorn
        import cv2
        import numpy
        import bcrypt
        print("✅ Basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_startup():
    """Test that the FastAPI app can start"""
    print("Testing app startup...")
    try:
        # Add backend to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.main import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ App startup error: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("Testing database...")
    try:
        from backend import database_handler
        database_handler.initialize_database()
        print("✅ Database initialization successful")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running pre-deployment tests...\n")
    
    tests = [
        test_imports,
        test_app_startup,
        test_database
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    if all(results):
        print("🎉 All tests passed! Ready for deployment to Render.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())