@echo off
REM Build Knight Online Demo Installer executable
REM Requires Python 3.8+ and PyInstaller

echo ==========================================
echo   Knight Online Demo - Installer Builder
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Install PyInstaller if needed
echo Installing/Updating PyInstaller...
pip install pyinstaller --upgrade --quiet

REM Build installer
echo.
echo Building installer executable...
cd /d "%~dp0"

pyinstaller --onefile --windowed ^
    --name "KO-Demo-Setup" ^
    --icon "../assets/icon.ico" ^
    KO-Demo-Installer.py

if errorlevel 1 (
    REM Try without icon if it fails
    pyinstaller --onefile --windowed ^
        --name "KO-Demo-Setup" ^
        KO-Demo-Installer.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Build complete!
echo   Installer: dist\KO-Demo-Setup.exe
echo ==========================================
pause
