import email
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_pytest.utils.Common import robust_click


class signInPage:
    def __init__(self, driver):
        self.driver = driver
        # LinkedIn frequently toggles between these sets of IDs
        self.email_or_phone_number_box = (By.NAME, "session_key") 
        self.email_or_phone_number_box_alt = (By.ID, "username")
    
        self.password_box = (By.ID, "session_password")
        self.password_box_alt = (By.ID, "password")
    
        self.submit_button = (By.XPATH, "//button[@type='submit']")
    
 
    def enter_email(self, email="babidash252@gmail.com"):

        try:
            email_input = robust_click(
            self,
            self.email_or_phone_number_box
        )

        except Exception:
            email_input = robust_click(
            self,
            self.email_or_phone_number_box_alt
        )

        email_input.clear()

        time.sleep(1)

        email_input.send_keys(email)

    print("Email entered successfully")
       
 
    def enter_password(self, password="Babi@252dash"):
        wait = WebDriverWait(self.driver, 10)
        try:
            password_input = wait.until(EC.element_to_be_clickable(self.password_box))
        except:            
            password_input = wait.until(EC.element_to_be_clickable(self.password_box_alt))
            
        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

    def dismiss_post_login_popup(self):
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            time.sleep(1)
            return True
        except Exception:
            pass

        post_login_locators = [
            (By.XPATH, "//button[contains(., 'Not now') or contains(., 'Skip') or contains(., 'Maybe later') or contains(., 'No thanks') or contains(., 'Close') or contains(., 'Dismiss') or contains(., 'Later') or contains(., 'Continue without') ]"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, "button[aria-label='Dismiss']"),
            (By.CSS_SELECTOR, "button.artdeco-modal__dismiss"),
        ]
        for locator in post_login_locators:
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                self.safe_click(button)
                time.sleep(1)
                return True
            except Exception:
                continue
        return False

    def click_submit_button(self):
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        )
        submit_btn.click()
        time.sleep(2)
        self.dismiss_post_login_popup()