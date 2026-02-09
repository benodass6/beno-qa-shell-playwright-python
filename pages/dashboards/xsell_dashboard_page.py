from utils.helpers import log_message, capture_and_attach
from pages.base_page import BasePage


class XSellDashboardPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    XSELL_DASHBOARD_LINK = "X-Sell Dashboard badge {\"svg"
    CHART_LABELS = ".fusioncharts-datalabels text"

    # ========================================================
    # METHODS
    # ========================================================

    def open_and_validate(self):
        self.page.get_by_role("link", name=self.XSELL_DASHBOARD_LINK).click()
        self.wait_for(self.CHART_LABELS, timeout=180000)
        self.page.wait_for_timeout(180000)

        capture_and_attach(
            self.page,
            "6_Xshell Dashboard.png",
            "X-Sell Dashboard",
            full_page=True,
        )
        log_message("X-Sell Dashboard loaded successfully.")
