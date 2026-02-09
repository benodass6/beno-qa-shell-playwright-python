from utils.helpers import log_message, capture_and_attach


class BasePage:
    def __init__(self, page):
        self.page = page

    def wait_for(self, selector: str, timeout: int = 60000):
        log_message(f"Waiting for element: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_xpath(self, xpath: str, timeout: int = 60000):
        self.wait_for(xpath, timeout)
        self.page.locator(xpath).click()

    def get_text(self, xpath: str, timeout: int = 60000) -> str:
        self.wait_for(xpath, timeout)
        return self.page.locator(xpath).inner_text().strip()

    def screenshot(self, filename: str, name: str, full_page: bool = True):
        capture_and_attach(self.page, filename, name, full_page)

    def wait_for_timeout(self, timeout: int):
        self.page.wait_for_timeout(timeout)
