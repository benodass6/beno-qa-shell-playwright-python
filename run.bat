@echo off
TITLE Running Automation Framework

echo ===============================================
echo 🔄 CLEANING OLD REPORTS
echo ===============================================

IF EXIST reports\allure (
    rmdir /S /Q reports\allure
)
IF EXIST reports\allure-report (
    rmdir /S /Q reports\allure-report
)
IF EXIST Allure_Final_Report.pdf (
    del /Q Allure_Final_Report.pdf
)

echo ===============================================
echo 🚀 RUNNING TESTS...
echo ===============================================
CALL .\.venv\Scripts\pytest.exe -v --alluredir=reports/allure

echo.
echo ===============================================
echo 📊 GENERATING ALLURE REPORT
echo ===============================================
allure generate reports/allure -o reports/allure-report --clean

echo.
echo ===============================================
echo 🌐 OPENING ALLURE REPORT
echo ===============================================
allure open reports/allure-report

echo.
echo ===============================================
echo ✅ Automation Execution Completed
echo ===============================================

pause

