@echo off
cd frontend
echo Setting up development mode with ESLint warnings disabled...
echo ESLINT_NO_DEV_ERRORS=true > .env
echo ESLINT_NO_DEV_WARNINGS=true >> .env
echo FAST_REFRESH=false >> .env
echo BROWSER=none >> .env

echo Starting React app in development mode...
npm start 