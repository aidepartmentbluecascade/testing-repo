@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 server.py
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3 was not found. Install Python 3.10 or newer for the optional server.
    echo Open index.html directly for offline learning.
  ) else (
    python server.py
  )
)
pause
