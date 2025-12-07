@echo off
echo ===================================================
echo   Football League Management System - Setup
echo ===================================================

echo.
echo [1/4] Installing Root Dependencies...
call npm install
if %errorlevel% neq 0 goto :error

echo.
echo [2/4] Installing Backend Dependencies...
cd backend
call npm install
if %errorlevel% neq 0 goto :error
cd ..

echo.
echo [3/4] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 goto :error
cd ..

echo.
echo [4/4] Setting up Database...
cd backend
call node scripts/reset_db.js
if %errorlevel% neq 0 goto :error
cd ..

echo.
echo ===================================================
echo   Setup Complete!
echo   Run 'npm run dev' to start the application.
echo ===================================================
pause
exit /b 0

:error
echo.
echo [ERROR] Setup failed. Please check the error messages above.
pause
exit /b 1
