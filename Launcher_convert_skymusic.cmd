@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%SCRIPT_DIR%.venv\Scripts\python.exe"
set "TARGET_SCRIPT=%SCRIPT_DIR%convert_skymusic.py"

if not exist "%PYTHON_EXE%" (
    echo Python virtual environment not found:
    echo   "%PYTHON_EXE%"
    pause
    exit /b 1
)

pushd "%SCRIPT_DIR%" >nul
"%PYTHON_EXE%" "%TARGET_SCRIPT%" %*
set "EXIT_CODE=%ERRORLEVEL%"
popd >nul

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Script exited with code %EXIT_CODE%.
    pause
)

exit /b %EXIT_CODE%
