# 🚀 Two-Phase Render Deployment Strategy

## Phase 1: Minimal Deployment (Do this first!)

This gets the basic API running without heavy ML dependencies.

### Step 1: Update Render Settings

**In your Render dashboard, change these settings:**

- **Start Command**: `python main_minimal.py`
- **Build Command**: 
  ```bash
  python -m pip install --upgrade pip && pip install setuptools>=70.0.0 wheel>=0.41.0 && pip install -r requirements_basic.txt
  ```

### Step 2: Test Basic Functionality

Once deployed, test these endpoints:
- `GET /` - Should return basic status
- `GET /health` - Health check
- `GET /api/auth/` - Basic auth endpoints

---

## Phase 2: Full Deployment (After Phase 1 works)

Once the minimal version is working, we'll gradually add back features.

### Step 1: Switch to Full Requirements

Change Render settings to:
- **Start Command**: `python main.py`
- **Build Command**: 
  ```bash
  python -m pip install --upgrade pip && pip install setuptools>=70.0.0 wheel>=0.41.0 && pip install -r requirements.txt
  ```

### Step 2: Monitor and Debug

Watch the build logs carefully and fix any dependency issues.

---

## Current Files for Phase 1:

- ✅ `requirements_basic.txt` - Minimal dependencies
- ✅ `main_minimal.py` - Entry point without ML features
- ✅ `backend/main_minimal.py` - Minimal FastAPI app

## Quick Commands:

```bash
# Commit current changes
git add .
git commit -m "Add minimal deployment strategy for Render"
git push origin main
```

Then update Render to use Phase 1 settings!