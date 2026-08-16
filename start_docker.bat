@echo off
title Theatre Ticket System - Docker Launcher
echo ========================================================
echo        Theatre Ticketing System - Docker Launcher
echo ========================================================
echo.

:: Check if Docker daemon is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Desktop is not running! 
    echo Please open Docker Desktop first, then run this script again.
    echo.
    pause
    exit /b 1
)

echo [1/3] Building and starting Docker containers...
docker compose up --build -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker containers. Check Docker Desktop for errors.
    pause
    exit /b 1
)

echo.
echo [2/3] Server started successfully on port 5000!
echo [3/3] Opening browser preview...
start http://localhost:5000

echo.
echo ========================================================
echo System is fully active in the background. You can close this window.
echo To shut down the containers, run 'stop_docker.bat'.
echo ========================================================
echo.
pause
