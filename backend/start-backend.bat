@echo off
echo Starting FastAPI backend with optimized settings...

cd backend

REM Check if Python virtual environment exists and activate it
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

REM Set performance optimization environment variables
set ENVIRONMENT=development
set DEBUG=false
set WEB_CONCURRENCY=2
set PORT=8000
set HOST=0.0.0.0
set PYTHONOPTIMIZE=1

REM Start the FastAPI application with uvicorn
echo Starting backend on http://localhost:%PORT%
python -m uvicorn main:app --reload --host %HOST% --port %PORT% --workers %WEB_CONCURRENCY% --log-level info

REM Deactivate virtual environment when server stops
call venv\Scripts\deactivate.bat 