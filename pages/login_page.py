from utils.helpers import log_message
from .base_page import BasePage


class LoginPage(BasePage):

    # ========================================================
    # LOCATORS - All Login Page Locators/XPaths
    # ========================================================
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button:has-text('Log in')"
    CANCEL_DIALOG_BUTTON = "button:has-text('Cancel Dialog')"

    # ========================================================
    # METHODS
    # ========================================================

    def goto_login_page(self, url: str):
        """Navigate to login page"""
        log_message(f"Navigating to: {url}")
        self.page.goto(url, timeout=180000, wait_until="domcontentloaded")

    def login_global_user(self, email: str, password: str):
        """Login with global user credentials"""
        log_message("Logging in user...")
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
        log_message(f"User logged in successfully: {email}")

        # Handle popup dialog if present
        try:
            self.page.get_by_role("button", name="Cancel Dialog").click()
            log_message("Closed pop-up dialog.")
        except Exception:
            log_message("Popup not displayed. Continuing...", level="WARN")

