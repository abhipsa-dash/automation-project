from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""This will contain all details, functions and xpaths related to the homepage"""

class homePage:
    def __init__(self, driver):
        self.driver = driver

    # Xpath for the profile icon
    profile_icon_xpath = "//li[@class='_100ad682 _9e42b625 d801f263 _6088119d'][6]"

    # Xpath for the Sign Out button
    sign_out_button_xpath = "//p[text()='Sign out']"

    def click_profile_icon(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.profile_icon_xpath))
        ).click()

    def click_sign_out_button(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.sign_out_button_xpath))
        ).click()