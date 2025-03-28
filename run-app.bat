@echo off
echo Starting Smart Rent Platform...

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8+ and try again.
    exit /b 1
)

:: Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js is not installed or not in PATH. Please install Node.js 14+ and try again.
    exit /b 1
)

echo Starting backend in a new window...
start "Smart Rent Backend" cmd /k "start-backend.bat"

:: Wait a bit for the backend to start
timeout /t 5 /nobreak > nul

echo Starting frontend in a new window...
start "Smart Rent Frontend" cmd /k "start-frontend.bat"

echo Smart Rent Platform started successfully!
echo Backend is available at: http://localhost:8000
echo Frontend is available at: http://localhost:3000

:: Keep this window open
pause 