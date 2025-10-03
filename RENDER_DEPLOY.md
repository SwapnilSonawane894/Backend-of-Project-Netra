# 📋 Render Deployment - Use Original Repository Structure

## 🚀 Render Dashboard Settings

### **Build Command (Try Option 1 first, then Option 2 if it fails):**

**Option 1 - Full features:**
```bash
python --version && pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
```

**Option 2 - Basic features (if Option 1 fails):**
```bash
python --version && pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements_working.txt
```

### **Start Command:**
```bash
python main.py
```

### **Environment Variables:**
```
PYTHON_VERSION=3.11.9
PORT=10000
```

### **Other Settings:**
- **Environment**: Python 3
- **Runtime**: Python
- **Plan**: Free
- **Auto-Deploy**: Yes
- **Health Check Path**: `/`

## ✅ Key Points:

1. **Python 3.11 Forced** - Uses `nixpacks.toml` and `runtime.txt` to enforce Python 3.11.9
2. **Original Structure** - Uses your original `backend/main.py` with all routes
3. **All Dependencies** - Includes full ML stack (OpenCV, TensorFlow, DeepFace)
4. **Database Included** - Your `data/project_netra_final.db` file is deployed

## 📂 Files Used:

- ✅ `main.py` - Original entry point
- ✅ `backend/main.py` - Original FastAPI app with all routes
- ✅ `backend/routes/` - All original route modules
- ✅ `requirements.txt` - Python 3.11 compatible versions
- ✅ `runtime.txt` - Python 3.11.9
- ✅ `nixpacks.toml` - Build configuration for Python 3.11
- ✅ `data/project_netra_final.db` - Your database

## 🎯 Expected Result:

All your original endpoints will work:
- `/api/auth/login`
- `/api/management/timetable`
- `/api/management/students`
- `/api/attendance/*`
- `/api/registration/*`
- `/api/principal/*`
- `/api/hod/*`
- `/api/staff/*`
- `/api/users/*`