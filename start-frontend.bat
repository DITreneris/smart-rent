@echo off
echo Starting Smart Rent Frontend...

cd frontend

echo Installing dependencies...
call npm install

echo Starting the frontend server...
call npm start

echo Frontend server shutdown. 