from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class signInPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_or_phone_number_box = (By.XPATH, "//input[@type='email']")
        self.password_box = (By.XPATH, "//input[@type='password']")
        self.submit_button = (By.XPATH, "//button[@type='submit']")

    def enter_email(self, email="babidash252@gmail.com"):
        email_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.email_or_phone_number_box)
        )
        email_input.click()
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password="Babi@252dash"):
        password_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.password_box)
        )
        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

    def click_submit_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        ).click()