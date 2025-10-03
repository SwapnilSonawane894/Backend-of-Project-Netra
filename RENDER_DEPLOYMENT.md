# Render Deployment Guide for Project Netra Backend

## Quick Deployment Steps

1. **Push changes to GitHub** (if not already done)
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" > "Web Service"
   - Connect your GitHub repo: `SwapnilSonawane894/Backend-of-Project-Netra`

3. **Configure Render Settings**:
   - **Name**: `project-netra-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **Environment Variables** (Add these in Render dashboard):
   ```
   PORT=10000
   PYTHON_VERSION=3.11.9
   ```

5. **Advanced Settings**:
   - **Plan**: Free (or Starter if you need more resources)
   - **Health Check Path**: `/`
   - **Auto-Deploy**: Yes

## Files Changed for Render Compatibility

- ✅ `requirements.txt` - Added build tools (setuptools, wheel)
- ✅ `main.py` - Updated port handling for Render
- ✅ `Procfile` - Updated for Render
- ✅ `render.yaml` - Added Render configuration
- ✅ `build.sh` - Custom build script
- ✅ `nixpacks.toml` - Build configuration
- ✅ `.python-version` - Python version specification

## Key Changes Made

1. **Fixed setuptools.build_meta error** by adding build dependencies
2. **Changed tensorflow to tensorflow-cpu** for better Render compatibility
3. **Updated port handling** to use Render's PORT environment variable
4. **Added build configuration files** for Render deployment

## Troubleshooting

If deployment fails:
1. Check the build logs in Render dashboard
2. Ensure all files are committed and pushed to GitHub
3. Try using `requirements_render.txt` if the main requirements.txt fails
4. Contact Render support if issues persist

## Alternative Requirements File

If the main requirements.txt fails, try renaming `requirements_render.txt` to `requirements.txt` - it has a more minimal set of dependencies optimized for Render.