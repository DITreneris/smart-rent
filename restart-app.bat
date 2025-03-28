@echo off
echo Smart Rent App Restart Script

echo Stopping any running processes...
taskkill /F /IM node.exe 2>nul

echo Setting up performance optimizations...
echo Adding performance environment variables...

:: Set environment variables for better performance
set NODE_ENV=production
set NODE_OPTIONS=--max-old-space-size=4096 --openssl-legacy-provider

cd frontend
echo Installing any missing dependencies...
call npm install

echo Starting the development server...
call npm start

cd ..

pause 