import os
from datetime import datetime

import allure
from allure_commons.types import AttachmentType


# ------------------------------
# Ensure screenshot folder exists
# ------------------------------
def _get_screenshot_path(filename: str) -> str:
    # Store all screenshots under reports/screenshots
    base_dir = os.path.join("reports", "screenshots")
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)


# ------------------------------
# LOG MESSAGE (Console + Allure)
# ------------------------------
def log_message(message: str, level: str = "INFO"):
    print(message)
    allure.attach(
        body=message,
        name=f"{level}: {message}",
        attachment_type=AttachmentType.TEXT,
    )


# ------------------------------
# SCREENSHOT ATTACH
# ------------------------------
def capture_and_attach(target, filename: str, name: str, full_page: bool = True):
    """
    target: page or locator
    filename: logical name like "1_sales_pipeline_dashboard.png"
    name: human-readable name in Allure
    """
    path = _get_screenshot_path(filename)

    screenshot_kwargs = {"path": path}
    # If it's a Page (has context attribute), support full_page screenshot
    if hasattr(target, "context"):
        screenshot_kwargs["full_page"] = full_page

    target.screenshot(**screenshot_kwargs)

    allure.attach.file(path, name=name, attachment_type=AttachmentType.PNG)
    log_message(f"[SCREENSHOT] Screenshot saved: {path}")


# ------------------------------
# RECORD RESULT
# ------------------------------
def record_result(condition: bool, success_msg: str, failure_msg: str, errors: list):
    if condition:
        log_message(success_msg, level="PASS")
    else:
        log_message(failure_msg, level="FAIL")
        errors.append(failure_msg)


# ------------------------------
# SAFE STEP WRAPPER
# ------------------------------
def safe_allure_step(step_name: str, errors: list, func):
    """
    Execute each step safely:
    - If step fails → log + append error
    - Continue to next step (test never stops in middle)
    - At end, test will fail once if errors list is non-empty
    """
    with allure.step(step_name):
        log_message(f"[START] START: {step_name}")
        try:
            func()
            log_message(f"[PASS] SUCCESS: {step_name}", level="PASS")
        except Exception as e:
            msg = f"[FAIL] FAILED: {step_name} — {str(e)}"
            log_message(msg, level="FAIL")
            errors.append(msg)

