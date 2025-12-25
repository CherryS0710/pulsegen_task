# Quick Start Guide

## Step 1: Install Dependencies

### Frontend (if not already done)
```bash
cd frontend
npm install
```

### Backend (if not already done)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Set Up Environment

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Step 3: Start Both Servers

You need **TWO terminal windows**:

### Terminal 1 - Backend Server
```bash
./start-backend.sh
```
OR manually:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 - Frontend Server
```bash
./start-frontend.sh
```
OR manually:
```bash
cd frontend
npm run dev
```

You should see: `Local: http://localhost:3000`

## Step 4: Open in Browser

Once BOTH servers are running, open:
**http://localhost:3000**

## Troubleshooting

### "Site cannot be reached" Error

1. **Check if frontend is running:**
   - Look for "Local: http://localhost:3000" in your terminal
   - If not running, start it with `npm run dev` in the frontend directory

2. **Check if backend is running:**
   - Look for "Uvicorn running on http://0.0.0.0:8000" in your terminal
   - If not running, start it with `uvicorn main:app --reload` in the backend directory

3. **Check port conflicts:**
   - Frontend needs port 3000
   - Backend needs port 8000
   - If ports are in use, you'll see an error message

4. **Verify both terminals are running:**
   - You MUST have both servers running simultaneously
   - Frontend alone won't work - it needs the backend API

### API Errors

- Make sure `.env` file exists with a valid `OPENAI_API_KEY`
- Check backend terminal for error messages
- Verify backend is accessible at `http://localhost:8000`

### Still Having Issues?

1. Check terminal output for error messages
2. Verify Python 3.10+ is installed: `python3 --version`
3. Verify Node.js 18+ is installed: `node --version`
4. Make sure all dependencies are installed


