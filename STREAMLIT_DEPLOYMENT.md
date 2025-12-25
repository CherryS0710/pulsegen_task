# Streamlit Deployment Guide

## Overview

This guide explains how to deploy the Module Extraction AI application using Streamlit. The Streamlit version provides a Python-based UI that connects to the same FastAPI backend.

## Architecture

- **Streamlit Frontend**: Python-based web UI (`streamlit_app.py`)
- **FastAPI Backend**: Same backend as before (`backend/main.py`)
- **Deployment Options**: 
  1. Local (both on same machine)
  2. Streamlit Cloud (frontend) + Backend (separate server)
  3. Single Streamlit app with embedded backend

## Option 1: Local Deployment (Development)

### Step 1: Install Dependencies

```bash
# Install Streamlit and dependencies
pip install -r requirements-streamlit.txt

# Or install just Streamlit for frontend
pip install streamlit requests
```

### Step 2: Start Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Streamlit App

```bash
# From project root
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## Option 2: Streamlit Cloud Deployment (Recommended)

### Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at https://streamlit.io/cloud)
3. Backend deployed somewhere accessible (or use embedded option)

### Step 1: Prepare Repository

1. Push your code to GitHub
2. Make sure these files are in the repo:
   - `streamlit_app.py`
   - `backend/` directory
   - `requirements-streamlit.txt` or `requirements.txt`
   - `.env.example` (for reference)

### Step 2: Deploy Backend Separately

You need to deploy the backend somewhere accessible:

**Option A: Railway**
1. Go to https://railway.app
2. Create new project
3. Connect GitHub repo
4. Set root directory to `backend`
5. Add environment variables from `.env`
6. Deploy

**Option B: Render**
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Set root directory to `backend`
5. Add environment variables
6. Deploy

**Option C: Heroku**
1. Create `Procfile` in backend:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy to Heroku

### Step 3: Deploy Streamlit App

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Set:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.10 or 3.11
5. Add secrets (if needed):
   - Go to Settings → Secrets
   - Add backend URL if different from default
6. Deploy!

### Step 4: Configure Backend URL

In Streamlit Cloud:
- Go to app settings
- Add secret: `BACKEND_URL` = your backend URL
- Update `streamlit_app.py` to read from secrets:

```python
import streamlit as st

# Read from secrets or use default
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")
```

## Option 3: Embedded Backend (Single App)

For simpler deployment, you can embed the backend logic directly in Streamlit:

### Modified streamlit_app.py

```python
# Add backend imports at top
import sys
sys.path.append('backend')
from services.crawler import DocumentationCrawler
from services.extractor import ModuleExtractor
import asyncio

# Replace extract_modules function with direct calls
async def extract_modules_direct(urls):
    crawler = DocumentationCrawler()
    extractor = ModuleExtractor()
    
    all_content = []
    for url in urls:
        content = await crawler.crawl_documentation(url)
        if content:
            all_content.append({"url": url, "content": content})
    
    if all_content:
        modules = await extractor.extract_modules(all_content)
        return {"modules": modules}
    return None
```

Then use `asyncio.run()` to call it.

## Environment Variables

### For Streamlit Cloud

Add secrets in Streamlit Cloud dashboard:
- `OPENAI_API_KEY`: Your API key
- `OPENAI_API_BASE`: API base URL (if using Groq, etc.)
- `OPENAI_MODEL`: Model name
- `BACKEND_URL`: Backend API URL (if using separate backend)

### For Local Development

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_API_BASE = "https://api.groq.com/openai/v1"
OPENAI_MODEL = "llama-3.1-8b-instant"
BACKEND_URL = "http://localhost:8000"
```

## File Structure for Deployment

```
pulsegen.io/
├── streamlit_app.py          # Streamlit frontend
├── requirements-streamlit.txt # Dependencies
├── backend/
│   ├── main.py               # FastAPI backend
│   ├── services/
│   │   ├── crawler.py
│   │   └── extractor.py
│   └── requirements.txt
├── .streamlit/
│   └── secrets.toml          # Local secrets (not in git)
└── .env.example              # Example env file
```

## Quick Start Commands

### Local Development

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2: Streamlit
streamlit run streamlit_app.py
```

### Streamlit Cloud

1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Add secrets
4. Done!

## Troubleshooting

### Backend Connection Issues

- Check backend URL in Streamlit sidebar
- Verify backend is accessible (not localhost if deployed)
- Check CORS settings in backend

### API Key Issues

- Ensure secrets are set correctly
- Check `.env` file is loaded (for local)
- Verify API key format

### Timeout Issues

- Increase timeout in `streamlit_app.py`
- Check backend logs for errors
- Verify URLs are accessible

## Advantages of Streamlit

✅ Easy deployment (one command)  
✅ No frontend build process  
✅ Python-only stack  
✅ Built-in components  
✅ Free hosting on Streamlit Cloud  
✅ Easy to customize  

## Limitations

⚠️ Less customizable than React  
⚠️ Slower for complex UIs  
⚠️ Backend must be accessible (or embedded)  

## Next Steps

1. Test locally with `streamlit run streamlit_app.py`
2. Push to GitHub
3. Deploy to Streamlit Cloud
4. Configure backend URL
5. Share your app!

