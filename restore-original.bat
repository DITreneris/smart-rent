@echo off
cd frontend
echo Restoring original React app configuration...
if exist src\index-original.js (
  copy src\index-original.js src\index.js /Y
  echo Original index.js restored.
) else (
  echo WARNING: Original index.js backup not found.
  echo Using current index.js as a base.
)
echo Installing required dependencies...
call npm install react-router-dom
echo Starting React frontend...
call npm start 