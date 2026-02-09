from utils.helpers import log_message, capture_and_attach
from pages.base_page import BasePage


class DashboardViewPage(BasePage):

    # ========================================================
    # LOCATORS
    # ========================================================
    DASHBOARD_VIEW_LINK = "Dashboard View"
    TABLE_VALUE_XPATH = "(//tbody//tr[1]//td)[2]"
    CLUSTER_LEVEL_ICON = "(//md-icon[@aria-label='Click to ViewCluster Level'])[1]"
    COUNTRY_LEVEL_ICON = "(//md-icon[@aria-label='Click to ViewCountry Level'])[1]"
    SHELL_LOGO = "//h2[normalize-space()='Shell']"
    MAIN_DASHBOARD_TITLE = "(//span[normalize-space(text())='Sales & Pipeline Dashboard'])[1]"

    # ========================================================
    # METHODS
    # ========================================================

    def _navigate_to_main_dashboard(self):
        """Navigate back to main dashboard by clicking Shell logo"""
        self.page.locator(self.SHELL_LOGO).click()
        self.wait_for(self.MAIN_DASHBOARD_TITLE, timeout=180000)
        self.page.wait_for_timeout(3000)

    def get_region_dashboard_view(self):
        self._navigate_to_main_dashboard()
        self.page.get_by_text(self.DASHBOARD_VIEW_LINK, exact=True).first.click()
        self.page.wait_for_timeout(20000)

        self.wait_for(self.TABLE_VALUE_XPATH, timeout=60000)
        val = self.page.locator(self.TABLE_VALUE_XPATH).inner_text().strip()
        log_message(f"Dashboard View - Region Annual Target = {val}")

        capture_and_attach(
            self.page,
            "04_Dashboard_Region.png",
            "Dashboard View - Region Annual Target",
            full_page=True,
        )
        return val

    def get_cluster_dashboard_view(self):
        self.page.wait_for_selector(self.CLUSTER_LEVEL_ICON, timeout=120000).click()
        self.page.wait_for_timeout(10000)

        self.wait_for(self.TABLE_VALUE_XPATH, timeout=60000)
        val = self.page.locator(self.TABLE_VALUE_XPATH).inner_text().strip()
        log_message(f"Dashboard View - Cluster Annual Target = {val}")

        capture_and_attach(
            self.page,
            "05_Dashboard_Cluster.png",
            "Dashboard View - Cluster Annual Target",
            full_page=True,
        )
        return val

    def get_country_dashboard_view(self):
        self.page.wait_for_selector(self.COUNTRY_LEVEL_ICON, timeout=120000).click()
        self.page.wait_for_timeout(10000)

        self.wait_for(self.TABLE_VALUE_XPATH, timeout=60000)
        val = self.page.locator(self.TABLE_VALUE_XPATH).inner_text().strip()
        log_message(f"Dashboard View - Country Annual Target = {val}")

        capture_and_attach(
            self.page,
            "06_Dashboard_Country.png",
            "Dashboard View - Country Annual Target",
            full_page=True,
        )
        return val
