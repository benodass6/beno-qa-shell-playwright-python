# PowerShell Setup Script for Cl_Automation Project

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🚀 Setting Up Cl_Automation Project" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create Virtual Environment
Write-Host "Step 1: Creating Virtual Environment" -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment!" -ForegroundColor Red
        Write-Host "Please make sure Python is installed and added to PATH." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green
}
Write-Host ""

# Step 2: Activate Virtual Environment
Write-Host "Step 2: Activating Virtual Environment" -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
Write-Host ""

# Step 3: Upgrade pip
Write-Host "Step 3: Upgrading pip" -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✅ pip upgraded!" -ForegroundColor Green
Write-Host ""

# Step 4: Install Python Packages
Write-Host "Step 4: Installing Python Packages" -ForegroundColor Yellow
Write-Host "Installing requirements from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install requirements!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ All Python packages installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 5: Install Playwright Browsers
Write-Host "Step 5: Installing Playwright Browsers" -ForegroundColor Yellow
Write-Host "Installing Playwright browsers (this may take a few minutes)..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Playwright browsers!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Playwright browsers installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 6: Verify Installation
Write-Host "Step 6: Verifying Installation" -ForegroundColor Yellow
Write-Host "Checking installed packages..." -ForegroundColor Yellow
python -c "import pytest; print(f'✅ pytest version: {pytest.__version__}')"
python -c "import playwright; print(f'✅ playwright installed')"
python -c "import allure; print(f'✅ allure-pytest installed')"
Write-Host ""

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "✅ Setup Completed Successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run tests: .\run.bat" -ForegroundColor White
Write-Host "2. Or activate venv manually: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

