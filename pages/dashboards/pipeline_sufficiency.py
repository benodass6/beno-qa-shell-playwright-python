from utils.helpers import log_message, capture_and_attach, record_result
from pages.base_page import BasePage


class PipelineSufficiencyPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    ANNUAL_TARGET_XPATH = "(//p[text()='Annual']/following::p[text()='Target'][1]/ancestor::div[contains(@class,'widget-content')]//p[contains(@class,'kpi_charts_value1')])[1]"
    PIPELINE_SUFFICIENCY_LINK = "Pipeline Sufficiency"
    TARGET_2025_XPATH = "(//tr[td[contains(normalize-space(),'Target 2025')]]//td[contains(@class,'column_split_padding')])[2]"
    CHART_LABELS = ".fusioncharts-datalabels text"

    # ========================================================
    # METHODS
    # ========================================================

    def validate_annual_vs_pipeline_target(self, errors):
        self.wait_for(self.ANNUAL_TARGET_XPATH, timeout=15000)
        annual_val = self.page.locator(self.ANNUAL_TARGET_XPATH).inner_text().strip()
        log_message(f"Annual Target (Dashboard) = {annual_val}")

        self.page.get_by_role("link", name=self.PIPELINE_SUFFICIENCY_LINK).click()
        self.wait_for(self.TARGET_2025_XPATH, timeout=200000)
        self.wait_for(self.CHART_LABELS, timeout=180000)
        self.page.wait_for_timeout(10000)

        capture_and_attach(
            self.page,
            "4_pipeline_sufficiency_loaded.png",
            "Pipeline Sufficiency",
            full_page=True,
        )

        target_value = self.page.locator(self.TARGET_2025_XPATH).inner_text().strip()
        log_message(f"Target 2025 (Pipeline Sufficiency) = {target_value}")

        def clean_value(val: str):
            cleaned = val.replace(",", "").replace("KL", "").replace(" ", "").replace("\xa0", "")
            return int(cleaned) if cleaned.isdigit() else None

        annual_clean = clean_value(annual_val)
        target_clean = clean_value(target_value)

        record_result(
            annual_clean == target_clean,
            "Annual Target matches Pipeline Target 2025",
            f"Mismatch! Dashboard Annual Target={annual_clean}, Pipeline Target 2025={target_clean}",
            errors,
        )
