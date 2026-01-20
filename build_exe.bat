@echo off
REM Build script for Windows Command Prompt
REM For bash/Git Bash, use: bash build.sh
REM For any terminal, use: python build.py

cd /d "%~dp0"

echo ========================================
echo Building Photobooth EXE
echo ========================================
echo.
echo Working directory: %CD%
echo.

REM Use the Python build script
python build.py

if exist "dist\Photobooth-QR.exe" (
    echo.
    echo ========================================
    echo Build Complete!
    echo ========================================
    echo.
    echo The executable is located in: dist\Photobooth-QR.exe
    echo.
    echo You can now:
    echo 1. Run dist\Photobooth-QR.exe to test
    echo 2. Copy it to any Windows computer
    echo 3. On first run, it will show settings window
    echo.
) else (
    echo.
    echo ========================================
    echo Build Failed!
    echo ========================================
    echo.
    echo The EXE was not created. Check the errors above.
    echo.
)

pause
