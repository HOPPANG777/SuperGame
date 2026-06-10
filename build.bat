@echo off
REM Super Game — PyInstaller 빌드 (강의 14)
REM 결과: dist\SuperGame.exe + dist\assets\

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo venv not found. Run: python -m venv venv
    exit /b 1
)

echo Installing PyInstaller + Pillow...
venv\Scripts\pip.exe install pyinstaller pillow -q

echo Building SuperGame.exe...
venv\Scripts\pyinstaller.exe -w -F ^
    --name=SuperGame ^
    --icon=assets\images\HOPPANG_2.png ^
    game.py

if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo Copying assets folder...
if exist "dist\assets" rmdir /s /q "dist\assets"
xcopy /E /I /Y "assets" "dist\assets" >nul

echo.
echo Done: dist\SuperGame.exe
echo       dist\assets\
echo Zip dist folder for submission.
