import os
import json
import smtplib
import ssl
from pathlib import Path
from datetime import datetime
from email.message import EmailMessage

import pytest
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ============================================================
#              CONFIGURATION
# ============================================================
ALLURE_RESULTS_DIR = "reports/allure"
PDF_OUTPUT = "Allure_Final_Report.pdf"

SEND_EMAIL = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "beno.a@amshuhu.com"
SENDER_PASSWORD = "pbefecenhkayqkcx"  # your app password
RECEIVER_EMAIL = "beno.a@amshuhu.com"
# RECEIVER_EMAIL = ["beno.a@amshuhu.com", "punitha.a@amshuhu.com", "aravindan@amshuhu.com"]  # Multiple emails allowed


# ============================================================
# PLAYWRIGHT FIXTURE
# ============================================================
@pytest.fixture
def page(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


# ============================================================
# PARSE ALLURE RESULTS
# ============================================================
def load_allure_results(directory):
    results = []
    for file in Path(directory).glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            if "name" not in data or "status" not in data:
                continue
            results.append(
                {
                    "name": data.get("name", "Unknown Test"),
                    "status": data.get("status", "unknown"),
                    "steps": data.get("steps", []),
                    "attachments": data.get("attachments", []),
                    "message": data.get("statusDetails", {}).get("message", ""),
                }
            )
        except Exception:
            continue
    return results


# ============================================================
# RESIZE IMAGE FOR PDF
# ============================================================
def resize_image_for_pdf(path):
    if not os.path.exists(path):
        return None
    try:
        from reportlab.platypus import Image as RLImage

        with Image.open(path) as img:
            w, h = img.size
            max_w, max_h = 500, 350
            scale = min(max_w / w, max_h / h, 1)
            new_w, new_h = int(w * scale), int(h * scale)
        return RLImage(path, width=new_w, height=new_h)
    except Exception:
        return None


# ============================================================
# BUILD PDF
# ============================================================
def generate_pdf(results, directory, output_file):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Mono", fontName="Courier", fontSize=9))

    doc = SimpleDocTemplate(output_file, pagesize=A4)
    story = []

    story.append(Paragraph("<b>Automation Test Execution Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 20))

    passed = sum(1 for t in results if t["status"] == "passed")
    failed = sum(1 for t in results if t["status"] == "failed")
    broken = sum(1 for t in results if t["status"] == "broken")
    skipped = sum(1 for t in results if t["status"] == "skipped")
    total = len(results)

    summary_table = Table(
     [
        ["Total Tests", total],
        ["Passed", passed],
        ["Failed", failed],
        ["Broken", broken],
        ["Skipped", skipped],
     ]
)


    summary_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 20))

    for test in results:
        story.append(
            Paragraph(f"<b>Test:</b> {test['name']}", styles["Heading2"])
        )
        story.append(
            Paragraph(f"<b>Status:</b> {test['status']}", styles["Normal"])
        )

        if test["message"]:
            story.append(Paragraph("<b>Failure Reason:</b>", styles["Heading3"]))
            # Escape HTML special characters to prevent parsing errors
            import html
            safe_message = html.escape(test["message"])
            story.append(Paragraph(safe_message, styles["Mono"]))

        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Steps:</b>", styles["Heading3"]))

        for step in test["steps"]:
            story.append(
                Paragraph(f"- {step.get('name', '')}", styles["Normal"])
            )
            for att in step.get("attachments", []):
                src = att.get("source")
                if not src:
                    continue
                path = os.path.join(directory, src)
                img = resize_image_for_pdf(path)
                if img:
                    story.append(Spacer(1, 10))
                    story.append(img)

        story.append(PageBreak())

    doc.build(story)
    print(f"[PDF] PDF Generated: {output_file}")


# ============================================================
# EMAIL PDF
# ============================================================
def send_pdf_email(file_path):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    # msg["To"] = ", ".join(RECEIVER_EMAIL) # Multiple emails allowed
    msg["Subject"] = "Automation Test Execution - PDF Report"
    msg.set_content(
        "Hi,\n\nPlease find attached the full execution report in PDF format.\n\nRegards,\nBeno A"
    )

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(file_path),
        )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("[EMAIL] Email Sent Successfully!")


# ============================================================
# PYTEST SESSION FINISH HOOK
# ============================================================
def pytest_sessionfinish(session, exitstatus):
    print("\n[INFO] Collecting Allure results...")

    results = load_allure_results(ALLURE_RESULTS_DIR)
    if not results:
        print("[WARN] No Allure JSON found, skipping PDF generation.")
        return


    # ====================================================
    # SORT TEST CASES IN PROPER TC01 → TC19 ORDER
    # ====================================================
    def sort_key(test):
        name = test.get("name", "")
        try:
            # Extract test case number from title
            num = int(name.split(" - ")[0].replace("TC", ""))
            return num
        except:
            return 9999

    results = sorted(results, key=sort_key)

    print("[INFO] Generating PDF report...")
    generate_pdf(results, ALLURE_RESULTS_DIR, PDF_OUTPUT)

    if SEND_EMAIL:
        print("[INFO] Sending email with PDF...")
        send_pdf_email(PDF_OUTPUT)

        
                
# ============================================================
# SESSION-LEVEL BROWSER FIXTURE
# ============================================================
@pytest.fixture(scope="session")
def browser(playwright):
    """Session-level browser instance"""
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    yield browser
    browser.close()


# ============================================================
# SESSION-LEVEL LOGIN FIXTURE (Login once for ALL tests)
# =============================================================
from pages.login_page import LoginPage
from utils.config import BASE_URL, GLOBAL_USER_EMAIL, GLOBAL_USER_PASSWORD

@pytest.fixture(scope="session")
def session_page(browser):
    page = browser.new_page()

    login = LoginPage(page)
    login.goto_login_page(BASE_URL)
    login.login_global_user(GLOBAL_USER_EMAIL, GLOBAL_USER_PASSWORD)

    print("\n[INFO] Logged in once for ALL test cases\n")

    yield page
    page.close()
    
    
    
# ============================================================
# SESSION-LEVEL ANNUAL TARGETS STORE
# ============================================================
    
@pytest.fixture(scope="session")
def annual_targets_store():
    return {}



