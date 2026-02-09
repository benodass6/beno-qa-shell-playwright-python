from utils.helpers import log_message, capture_and_attach
from pages.base_page import BasePage


class SpancopDashboardPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    SPANCOP_DASHBOARD_LINK = "SPANCOP Dashboard"
    CHART_LABELS = ".fusioncharts-datalabels text"

    # ========================================================
    # METHODS
    # ========================================================

    def open_and_validate(self):
        self.page.get_by_role("link", name=self.SPANCOP_DASHBOARD_LINK).click()
        self.wait_for(self.CHART_LABELS, timeout=200000)
        self.page.wait_for_timeout(50000)

        capture_and_attach(
            self.page,
            "7_SPANCOP Dashboard.png",
            "SPANCOP Dashboard",
            full_page=True,
        )
        log_message("SPANCOP Dashboard loaded successfully.")
