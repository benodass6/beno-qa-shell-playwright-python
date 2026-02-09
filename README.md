# 🚀 Cl_Automation - Playwright Python POM Framework

UI Testing Framework with Allure Reports, PDF Reports, and Email Notifications

## 📋 Prerequisites

- **Python 3.8+** installed
- **Git** (optional, for version control)

## 🛠️ Setup Instructions

### Option 1: Automated Setup (Recommended)

#### For Windows (Batch):
```bash
setup.bat
```

#### For Windows (PowerShell):
```powershell
.\setup.ps1
```

### Option 2: Manual Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate Virtual Environment:**
   ```bash
   # Windows (CMD)
   .venv\Scripts\activate.bat
   
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Playwright Browsers:**
   ```bash
   playwright install chromium
   ```

## 📦 Installed Packages

- `playwright` - Browser automation
- `pytest` - Testing framework
- `allure-pytest` - Allure reporting
- `pytest-playwright` - Playwright integration
- `Pillow` - Image processing for PDF
- `reportlab` - PDF generation

## 🚀 Running Tests

### Run All Tests:
```bash
run.bat
```

### Run Specific Test:
```bash
.venv\Scripts\pytest.exe tests/test_dashboard_validations.py::test_main_dashboard_loaded -v
```

### Run with Allure:
```bash
.venv\Scripts\pytest.exe -v --alluredir=reports/allure
allure generate reports/allure -o reports/allure-report --clean
allure open reports/allure-report
```

## 📁 Project Structure

```
Cl_Automation/
├── pages/                    # Page Object Model
│   ├── base_page.py         # Base page class
│   ├── login_page.py        # Login page
│   ├── dashboards/          # Dashboard pages
│   └── reports/             # Report pages
├── tests/                    # Test files
│   └── test_dashboard_validations.py
├── utils/                    # Utilities
│   ├── config.py            # Configuration
│   └── helpers.py           # Helper functions
├── conftest.py              # Pytest configuration
├── pytest.ini               # Pytest settings
├── requirements.txt          # Python dependencies
├── run.bat                   # Test execution script
└── setup.bat                # Setup script
```

## ⚙️ Configuration

### Email Configuration (`conftest.py`):
- SMTP Server: `smtp.gmail.com`
- Port: `465`
- Sender: Configure in `conftest.py`
- Receivers: Configure in `conftest.py`

### Application Config (`utils/config.py`):
- Base URL: `https://shell3.isteer.co`
- Credentials: Configure in `utils/config.py`

## 📊 Reports

After test execution:
- **Allure Report**: `reports/allure-report/`
- **PDF Report**: `Allure_Final_Report.pdf`
- **Screenshots**: `reports/screenshots/`

## 🔧 Troubleshooting

### Virtual Environment Issues:
- Make sure Python is added to PATH
- Use `python --version` to verify Python installation

### Playwright Issues:
- Run `playwright install chromium` again
- Check internet connection for browser downloads

### Import Errors:
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## 📝 Notes

- Tests use session-level login (login once for all tests)
- Screenshots are automatically attached to Allure reports
- PDF report is automatically generated and emailed after execution

