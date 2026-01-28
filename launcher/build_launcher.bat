@echo off
REM Build Knight Online Demo Launcher executable
REM Requires Python 3.8+ and PyInstaller

echo ==========================================
echo   Knight Online Demo - Launcher Builder
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

REM Build launcher
echo.
echo Building launcher executable...
cd /d "%~dp0src"

pyinstaller --onefile --windowed ^
    --name "KO-Demo-Launcher" ^
    --icon "../icon.ico" ^
    --add-data "../icon.ico;." ^
    demo_launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

REM Copy to dist folder
echo.
echo Copying launcher to parent folder...
copy /y "dist\KO-Demo-Launcher.exe" "..\..\KO-Demo-Launcher.exe"

echo.
echo ==========================================
echo   Build complete!
echo   Launcher: KO-Demo-Launcher.exe
echo ==========================================
pause
