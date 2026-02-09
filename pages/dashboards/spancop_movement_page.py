from utils.helpers import log_message, capture_and_attach
from pages.base_page import BasePage


class SpancopMovementPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    SPANCOP_MOVEMENT_LINK = "SPANCOP Movement Dashboard"
    CHART_LABELS = ".fusioncharts-datalabels text"

    # ========================================================
    # METHODS
    # ========================================================

    def open_and_validate(self):
        self.page.get_by_role("link", name=self.SPANCOP_MOVEMENT_LINK).click()
        self.wait_for(self.CHART_LABELS, timeout=180000)
        self.page.wait_for_timeout(40000)

        capture_and_attach(
            self.page,
            "8_SPANCOP Movement Dashboard.png",
            "SPANCOP Movement Dashboard",
            full_page=True,
        )
        log_message("SPANCOP Movement Dashboard loaded successfully.")
        
        
