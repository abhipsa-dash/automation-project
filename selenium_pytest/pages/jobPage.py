"""This will contain job info, functions, and xpaths"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_pytest.utils.Common import robust_click


class jobPage:
    def __init__(self, driver):
        self.driver = driver

    # ── Jobs search / filter xpaths ───────────────────────────────────────────
    title_filter_xpath = "//button[contains(@aria-label,'Title filter')]"
    title_search_input_xpath = (
        "//input[contains(@aria-label,'Search by title') "
        "or contains(@placeholder,'Search by title')]"
    )
    title_add_input_xpath = (
        "//input[contains(@aria-label,'Add a title') "
        "or contains(@placeholder,'Add a title')]"
    )
    search_button_xpath = (
        "//button[contains(@class,'jobs-search-box__submit-button') "
        "or (contains(@aria-label,'Search') and @type='submit')]"
    )
    show_results_button_xpath = (
        "//button[contains(@aria-label,'Apply current filter') "
        "or normalize-space()='Show results']"
    )

    def _wait(self, timeout: int = 15):
        return WebDriverWait(self.driver, timeout)

    def click_title(self):
        """Open the Title filter or focus the title search field."""
        try:
            robust_click(self, (By.XPATH, self.title_filter_xpath)).click()
            self._wait().until(
                EC.visibility_of_element_located((By.XPATH, self.title_add_input_xpath))
            )
        except Exception:
            el = self._wait().until(
                EC.element_to_be_clickable((By.XPATH, self.title_search_input_xpath))
            )
            el.click()

    def enter_title(self, title: str):
        """Type the job title into the active title field."""
        for xpath in (self.title_add_input_xpath, self.title_search_input_xpath):
            try:
                el = self._wait().until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                el.click()
                el.send_keys(Keys.CONTROL + "a")
                el.send_keys(Keys.DELETE)
                el.send_keys(title)
                time.sleep(1)
                return
            except Exception:
                continue
        raise RuntimeError("Could not find a title input on the Jobs page")

    def click_search(self):
        """Submit the job search or apply the title filter."""
        for xpath in (self.show_results_button_xpath, self.search_button_xpath):
            try:
                robust_click(self, (By.XPATH, xpath)).click()
                time.sleep(3)
                return
            except Exception:
                continue
        raise RuntimeError("Could not find a Search button on the Jobs page")
