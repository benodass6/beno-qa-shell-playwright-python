@echo off
TITLE Setting Up Cl_Automation Project

echo ===============================================
echo 🚀 Setting Up Cl_Automation Project
echo ===============================================
echo.

echo ===============================================
echo Step 1: Creating Virtual Environment
echo ===============================================
if exist .venv (
    echo Virtual environment already exists. Skipping...
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment!
        echo Please make sure Python is installed and added to PATH.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully!
)
echo.

echo ===============================================
echo Step 2: Activating Virtual Environment
echo ===============================================
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)
echo ✅ Virtual environment activated!
echo.

echo ===============================================
echo Step 3: Upgrading pip
echo ===============================================
python -m pip install --upgrade pip
echo ✅ pip upgraded!
echo.

echo ===============================================
echo Step 4: Installing Python Packages
echo ===============================================
echo Installing requirements from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements!
    pause
    exit /b 1
)
echo ✅ All Python packages installed successfully!
echo.

echo ===============================================
echo Step 5: Installing Playwright Browsers
echo ===============================================
echo Installing Playwright browsers (this may take a few minutes)...
playwright install chromium
if errorlevel 1 (
    echo ❌ Failed to install Playwright browsers!
    pause
    exit /b 1
)
echo ✅ Playwright browsers installed successfully!
echo.

echo ===============================================
echo Step 6: Verifying Installation
echo ===============================================
echo Checking installed packages...
python -c "import pytest; print(f'✅ pytest version: {pytest.__version__}')"
python -c "import playwright; print(f'✅ playwright installed')"
python -c "import allure; print(f'✅ allure-pytest installed')"
echo.

echo ===============================================
echo ✅ Setup Completed Successfully!
echo ===============================================
echo.
echo Next steps:
echo 1. Run tests: run.bat
echo 2. Or activate venv manually: .venv\Scripts\activate.bat
echo.
pause

