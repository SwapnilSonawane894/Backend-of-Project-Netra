# 🚀 Render Deployment Checklist

## Pre-deployment Steps (Complete these first)

### 1. Test Locally
```bash
python test_deployment.py
```

### 2. Commit and Push Changes
```bash
git add .
git commit -m "Fix: Update configuration for Render deployment"
git push origin main
```

## Render Configuration

### 3. Create New Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository

### 4. Configure Service Settings
- **Name**: `project-netra-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Instance Type**: `Free` (or `Starter` for better performance)

### 5. Environment Variables (Add in Render Dashboard)
```
PORT=10000
PYTHON_VERSION=3.11.9
```

### 6. Advanced Settings
- **Auto-Deploy**: `Yes`
- **Health Check Path**: `/`

## Troubleshooting

### If Build Fails:
1. Try using `requirements_minimal.txt`:
   - Rename it to `requirements.txt`
   - Or update Build Command to: `pip install -r requirements_minimal.txt`

2. Check build logs for specific errors

3. Common fixes:
   - Ensure setuptools and wheel are installed first
   - Use tensorflow-cpu instead of tensorflow
   - Remove problematic packages temporarily

### If App Doesn't Start:
1. Check if PORT environment variable is set correctly
2. Verify the start command: `python main.py`
3. Check application logs in Render dashboard

## Success Indicators
- ✅ Build completes without errors
- ✅ Service starts successfully
- ✅ Health check passes at `/`
- ✅ API endpoints respond correctly

## Post-Deployment Testing
Once deployed, test these endpoints:
- `GET /` - Health check
- `GET /api/auth/test` - If available
- Check logs for any runtime errors

---
**Created for Project Netra - Backend Deployment**