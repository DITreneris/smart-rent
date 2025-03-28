@echo off
cd frontend
echo Rebuilding React app with fixed components...
echo ESLINT_NO_DEV_ERRORS=true > .env
npm run build
echo Build completed. Starting development server...
npm start 