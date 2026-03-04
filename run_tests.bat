@echo off
echo ==========================================
echo   Running Dash App Tests
echo ==========================================


cd /d "F:\The Forage\quantium\quantium-starter-repo"

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please create it first: python -m venv venv
    pause
    exit /b 1
)


set PYTHON=venv\Scripts\python.exe

%PYTHON% -c "import dash" >nul 2>&1
if errorlevel 1 (
    echo Installing dash and pytest in virtual environment...
    %PYTHON% -m pip install dash pandas plotly pytest
)

echo.
echo Running tests...
echo ------------------------------------------
%PYTHON% -m pytest test_app.py -v

if %ERRORLEVEL% == 0 (
    echo.
    echo ==========================================
    echo   All tests passed! 
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo   Some tests failed
    echo ==========================================
)

echo.
echo Done!
pause