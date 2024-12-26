@echo off
setlocal

REM Step 1: Create executable with PyInstaller
echo Creating executable with PyInstaller...
python -m PyInstaller main.py --windowed --onefile --add-data "utils;utils" --name "Blitz game" --icon "data/img/icon.ico"
if ERRORLEVEL 1 (
    echo PyInstaller encountered an error. Exiting...
    exit /b 1
)

REM Step 2: Copy the executable to the current directory
echo Copying executable to the current directory...
copy dist\"Blitz game.exe" "Blitz game.exe" 
if ERRORLEVEL 1 (
    echo Failed to copy the executable. Exiting...
    exit /b 1
)

REM Step 3: Clean up build files
echo Cleaning up build files...
rmdir /s /q build dist
del "Blitz game.spec" 
if ERRORLEVEL 1 (
    echo Cleanup encountered an error. Exiting...
    exit /b 1
)

echo Build process completed successfully.
exit /b 0
