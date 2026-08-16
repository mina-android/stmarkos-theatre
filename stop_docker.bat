@echo off
title Theatre Ticket System - Docker Shutdown
echo ========================================================
echo        Theatre Ticketing System - Docker Shutdown
echo ========================================================
echo.

echo Stopping and removing Docker containers...
docker compose down

if %errorlevel% neq 0 (
    echo [ERROR] Failed to shut down containers cleanly.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Containers stopped successfully!
echo ========================================================
echo.
pause
