@echo off
echo ===================================================
echo    SMART RENT PLATFORM - DIAGNOSTICS
echo ===================================================
echo.
echo Running system diagnostics...
echo.

echo SYSTEM INFORMATION:
echo -------------------
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
echo.

echo NETWORK INFORMATION:
echo -------------------
ipconfig | findstr /C:"IPv4 Address" /C:"Subnet Mask" /C:"Default Gateway"
echo.

echo CHECKING PORT STATUS:
echo -------------------
echo Checking if anything is already using ports 3000 or 8000...
netstat -ano | findstr "3000"
netstat -ano | findstr "8000"
echo.

echo CHECKING LOCALHOST CONNECTIVITY:
echo -------------------
ping -n 1 localhost
echo.

echo CHECKING FIREWALL STATUS:
echo -------------------
netsh advfirewall show currentprofile | findstr "State"
echo.

echo CHECKING NODE.JS INSTALLATION:
echo -------------------
node --version
npm --version
echo.

echo CHECKING PYTHON INSTALLATION:
echo -------------------
python --version
pip --version
echo.

echo CHECKING DIRECTORY STRUCTURE:
echo -------------------
if exist frontend (
  echo Frontend directory: FOUND
  if exist frontend\package.json (
    echo Frontend package.json: FOUND
  ) else (
    echo Frontend package.json: NOT FOUND - PROBLEM!
  )
  if exist frontend\node_modules (
    echo Frontend node_modules: FOUND
  ) else (
    echo Frontend node_modules: NOT FOUND - Run 'npm install' in frontend directory
  )
) else (
  echo Frontend directory: NOT FOUND - PROBLEM!
)

if exist backend (
  echo Backend directory: FOUND
  if exist backend\requirements.txt (
    echo Backend requirements.txt: FOUND
  ) else (
    echo Backend requirements.txt: NOT FOUND - PROBLEM!
  )
  if exist backend\venv (
    echo Backend virtual environment: FOUND
  ) else (
    echo Backend virtual environment: NOT FOUND - Run the setup script
  )
) else (
  echo Backend directory: NOT FOUND - PROBLEM!
)
echo.

echo TESTING BROWSER CONNECTION:
echo -------------------
echo Attempting to test localhost connections...
echo If you're having connection issues, try these troubleshooting steps:
echo 1. Make sure no other applications are using ports 3000 and 8000
echo 2. Check your firewall settings to allow these ports
echo 3. Run the frontend and backend separately using start-frontend.bat and start-backend.bat
echo 4. Ensure your antivirus is not blocking localhost connections
echo.

echo ===================================================
echo Diagnostic complete. Please review the information above.
echo =================================================== 