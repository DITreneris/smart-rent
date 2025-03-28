@echo off
echo Starting Smart Rent Backend...

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Starting the backend server...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo Backend server shutdown. 