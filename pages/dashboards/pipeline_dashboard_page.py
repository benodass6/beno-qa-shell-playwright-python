from utils.helpers import log_message, capture_and_attach
from pages.base_page import BasePage


class PipelineDashboardPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    REPORTS_BUTTON = "Reports"
    PIPELINE_DASHBOARD_LINK = "Pipeline Dashboard badge {\""
    CHART_LABELS = ".fusioncharts-datalabels text"

    # ========================================================
    # METHODS
    # ========================================================

    def open_and_validate(self):
        self.page.get_by_role("button", name=self.REPORTS_BUTTON).click()
        self.page.get_by_role("link", name=self.PIPELINE_DASHBOARD_LINK).click()
        self.wait_for(self.CHART_LABELS, timeout=180000)
        self.page.wait_for_timeout(60000)

        capture_and_attach(
            self.page,
            "5_pipeline_Dashboard.png",
            "Pipeline Dashboard",
            full_page=True,
        )
        log_message("Pipeline Dashboard loaded successfully.")
