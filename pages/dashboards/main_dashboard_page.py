from datetime import datetime, timedelta
from utils.helpers import log_message, capture_and_attach, record_result
from ..base_page import BasePage


class MainDashboardPage(BasePage):

    # ========================================================
    # LOCATORS - All Main Dashboard Locators/XPaths
    # ========================================================
    
    # Main Title
    MAIN_TITLE = "(//span[normalize-space(text())='Sales & Pipeline Dashboard'])[1]"

    # Hit Rate
    HIT_RATE = "//div[contains(@class,'hit_rate_per')]//span[contains(@class,'ng-binding')]"

    # Top Distributors
    TOP_DISTRIBUTOR_ROWS = "//label[normalize-space()='Top Distributors']/ancestor::md-card//tbody/tr"
    TOP_DISTRIBUTOR_NAMES = "//label[normalize-space()='Top Distributors']/ancestor::md-card//tbody/tr/td[1]"
    TOP_DISTRIBUTOR_CARD = "//label[normalize-space()='Top Distributors']/ancestor::md-card"

    # Top DSRs
    TOP_DSR_ROWS = "//label[normalize-space()='Top DSRs']/ancestor::md-card//tbody/tr"
    TOP_DSR_NAMES = "//label[normalize-space()='Top DSRs']/ancestor::md-card//tbody/tr/td[1]"
    TOP_DSR_CARD = "//label[normalize-space()='Top DSRs']/ancestor::md-card"

    # Previous Month
    PREV_MONTH_LABEL = "(//*[local-name()='text' and contains(., '-')])[1]"

    # Pipeline KPIs
    PIPELINE_KL = "(//div[@class='ng-scope layout-align-space-between-stretch layout-column flex-30']//p[contains(@class,'kpi_charts_value1')])[1]"
    PIPELINE_HASH = "(//div[@class='ng-scope layout-align-space-between-stretch layout-column flex-30']//p[contains(@class,'kpi_charts_value2')])[1]"
    PIPELINE_CYI = "(//div[@class='ng-scope layout-align-space-between-stretch layout-column flex-30']//p[contains(@class,'kpi_charts_value1')])[2]"

    # OPCYI vs WON
    OPCYI_BAR = "(//div[@class='bar-inner-new spancop_data'])[4]"
    WON_IMPACT = "(//div[contains(.,'Current Year Impact')]/following::p[contains(@class,'kpi_charts_value1')])[1]"

    # Annual Target
    ANNUAL_TARGET = "(//p[text()='Annual']/following::p[text()='Target'][1]/ancestor::div[contains(@class,'widget-content')]//p[contains(@class,'kpi_charts_value1')])[1]"

    # Region Reset
    REGION_SHELL_BTN = "//h2[normalize-space()='Shell']"

    # ========================================================
    # METHODS
    # ========================================================

    def verify_main_dashboard_loaded(self):
        """Verify Main Dashboard is loaded"""
        self.wait_for(self.MAIN_TITLE, timeout=180000)
        capture_and_attach(
            self.page,
            "1_sales_pipeline_dashboard.png",
            "Sales & Pipeline Dashboard",
            full_page=True,
        )
        log_message("[PASS] Global user dashboard loaded successfully.")

    def validate_hit_rate_non_zero(self, errors):
        """Validate Hit Rate is non-zero"""
        hit_rate = self.page.locator(self.HIT_RATE)
        hit_rate.wait_for(timeout=15000)

        value = hit_rate.inner_text().strip()
        log_message(f"[INFO] Hit Rate displayed on UI: = {value}")

        hit_rate_value = int(value.replace("%", ""))

        record_result(
            hit_rate_value != 0,
            "[PASS] Hit Rate is non-zero.",
            f"[FAIL] Hit Rate is ZERO! Found: {value}",
            errors,
        )

    def validate_top_distributors(self, errors):
        """Validate Top Distributors section"""
        self.wait_for(self.TOP_DISTRIBUTOR_ROWS, timeout=60000)

        dist_names = self.page.locator(self.TOP_DISTRIBUTOR_NAMES).all_inner_texts()
        log_message(f"Top Distributors: {dist_names}")

        for name in dist_names:
            record_result(
                "demo" not in name.lower(),
                f"[PASS] Distributor '{name}' valid.",
                f"[FAIL] Demo distributor found: {name}",
                errors,
            )

        dist_card = self.page.locator(self.TOP_DISTRIBUTOR_CARD)
        capture_and_attach(
            dist_card,
            "2_Top_Distributors.png",
            "Top Distributors",
            full_page=False,
        )

    def validate_top_dsr(self, errors):
        """Validate Top DSR section"""
        self.wait_for(self.TOP_DSR_ROWS, timeout=60000)

        names = self.page.locator(self.TOP_DSR_NAMES).all_inner_texts()
        log_message(f"Top DSRs: {names}")

        for n in names:
            record_result(
                "demo" not in n.lower(),
                f"[PASS] DSR '{n}' valid.",
                f"[FAIL] Demo DSR found: {n}",
                errors,
            )

        capture_and_attach(
            self.page.locator(self.TOP_DSR_CARD),
            "3_Top_DSRs.png",
            "Top DSRs",
            full_page=False,
        )

    def validate_previous_month(self, errors):
        """Validate Previous Month KPI"""
        today = datetime.today()
        first_day_this_month = today.replace(day=1)
        previous_month_last_day = first_day_this_month - timedelta(days=1)

        expected_month = previous_month_last_day.strftime("%B")
        expected_year = previous_month_last_day.strftime("%Y")
        expected_text = f"{expected_month} - {expected_year}"

        log_message(f"Expected Previous Month: {expected_text}")

        month_ui = self.page.locator(self.PREV_MONTH_LABEL)
        month_ui.wait_for()

        ui_text = month_ui.text_content().strip()
        log_message(f"Previous Month From UI: {ui_text}")

        record_result(
            ui_text == expected_text,
            f"[PASS] Previous month displayed correctly: {ui_text}",
            f"[FAIL] Expected {expected_text} but found {ui_text}",
            errors,
        )

    def validate_pipeline_size_limit(self, errors):
        """Validate Pipeline Size digit limits"""
        log_message("--- Pipeline Size Validation ---")

        pipeline_kl = self.page.locator(self.PIPELINE_KL).inner_text().strip()
        pipeline_hash = self.page.locator(self.PIPELINE_HASH).inner_text().strip()
        pipeline_cyi = self.page.locator(self.PIPELINE_CYI).inner_text().strip()

        log_message(f"Pipeline Size (KL): {pipeline_kl}")
        log_message(f"Pipeline Size (#): {pipeline_hash}")
        log_message(f"Pipeline Size CYI (KL): {pipeline_cyi}")

        def clean_number(v: str) -> int:
            return int(v.replace(",", ""))

        values = [
            ("Pipeline Size (KL)", clean_number(pipeline_kl)),
            ("Pipeline Size (#)", clean_number(pipeline_hash)),
            ("Pipeline Size CYI (KL)", clean_number(pipeline_cyi)),
        ]

        for label, val in values:
            record_result(
                val <= 9_999_999,
                f"[PASS] {label} is within 7-digit limit.",
                f"[FAIL] {label} exceeds 7 digits: {val:,}",
                errors,
            )

    def validate_opcyi_vs_won(self, errors):
        """Validate OPCYI equals WON Impact"""
        self.wait_for(self.OPCYI_BAR, timeout=15000)

        op_cyi_raw = self.page.locator(self.OPCYI_BAR).get_attribute("data-volume")
        op_cyi_clean = int(
            op_cyi_raw.replace(",", "").replace("KL", "").replace("\xa0", "")
        )
        log_message(f"OP CYI = {op_cyi_clean}")

        self.wait_for(self.WON_IMPACT, timeout=15000)

        won_raw = self.page.locator(self.WON_IMPACT).text_content().strip()
        won_clean = int(
            won_raw.replace(",", "").replace("KL", "").replace("\xa0", "")
        )
        log_message(f"WON Current Year Impact = {won_clean}")

        record_result(
            op_cyi_clean == won_clean,
            f"[PASS] Validation Passed: OP CYI = WON Current Year Impact = {won_clean}",
            f"[FAIL] Validation Failed: OP CYI ({op_cyi_clean}) != WON Current Year Impact ({won_clean})",
            errors,
        )

    def get_region_annual_main(self):
        """Get Region Annual Target from Main Dashboard"""
        self.page.locator(self.REGION_SHELL_BTN).click()
        self.wait_for(self.MAIN_TITLE, timeout=180000)

        self.wait_for(self.ANNUAL_TARGET, timeout=60000)
        val = self.page.locator(self.ANNUAL_TARGET).inner_text().strip()
        log_message(f"Region Level Annual Target = {val}")

        capture_and_attach(
            self.page,
            "01_main_dashboard_region.png",
            "Main Dashboard - Region Level Annual Target",
            full_page=True,
        )
        return val

    def get_cluster_annual_main(self):
        """Get Cluster Annual Target from Main Dashboard"""
        FILTERS_BUTTON = "//button[.//span[normalize-space()='Filters']]"
        REGION_SELECT = "//md-select[@name='region_name']"
        APAC_OPTION = "//md-option//div[normalize-space(text())='APAC']"
        SEARCH_BUTTON = "(//button[.//span[normalize-space()='Search']])[1]"

        self.page.locator(FILTERS_BUTTON).click()
        self.page.locator(REGION_SELECT).click()
        self.page.locator(APAC_OPTION).click()
        self.page.locator(SEARCH_BUTTON).click()
        self.page.wait_for_timeout(20000)

        self.wait_for(self.ANNUAL_TARGET, timeout=60000)
        val = self.page.locator(self.ANNUAL_TARGET).inner_text().strip()
        log_message(f"Cluster Level Annual Target = {val}")

        capture_and_attach(
            self.page,
            "02_cluster_level_dashboard.png",
            "Main Dashboard - Cluster Level Annual Target",
            full_page=True,
        )
        return val

    def get_country_annual_main(self):
        """Get Country Annual Target from Main Dashboard"""
        CLUSTER_SELECT = "//md-select[@name='cluster_name']"
        AP_MDS_OPTION = "//md-option//div[normalize-space(text())='AP MDs']"
        SEARCH_BUTTON = "(//button[.//span[normalize-space()='Search']])[1]"

        self.page.locator(CLUSTER_SELECT).click()
        self.page.locator(AP_MDS_OPTION).click()
        self.page.locator(SEARCH_BUTTON).click()
        self.page.wait_for_timeout(20000)

        self.wait_for(self.ANNUAL_TARGET, timeout=60000)
        val = self.page.locator(self.ANNUAL_TARGET).inner_text().strip()
        log_message(f"Country Level Annual Target = {val}")

        capture_and_attach(
            self.page,
            "03_country_level_dashboard.png",
            "Main Dashboard - Country Level Annual Target",
            full_page=True,
        )
        return val
