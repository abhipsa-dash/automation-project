import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class signInPage:
    def __init__(self, driver):
        self.driver = driver
        # LinkedIn frequently toggles between these sets of IDs
        self.email_or_phone_number_box = (By.ID, "session_key") 
        self.email_or_phone_number_box_alt = (By.ID, "username")
    
        self.password_box = (By.ID, "session_password")
        self.password_box_alt = (By.ID, "password")
    
        self.submit_button = (By.XPATH, "//button[@type='submit']")
    

    def safe_click(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].focus();", element)
            element.click()
            return
        except Exception:
            pass

        try:
            ActionChains(self.driver).move_to_element(element).click(element).perform()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].click();", element)

    def remove_page_overlays(self):
        self.driver.execute_script("document.querySelectorAll('div[role=dialog], div.modal, div[class*=overlay], div[class*=dialog], section[id*=cookie], section[class*=cookie], div[class*=sign-in], div[class*=signup]').forEach(el => el.remove());")

    def find_clickable_with_fallback(self, locators):
        for locator in locators:
            try:
                return WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(locator)
                )
            except Exception:
                continue
        raise Exception(f"Clickable element not found for locators: {locators}")

    def dismiss_popup(self):
        self.remove_page_overlays()
        popup_locators = [
            (By.XPATH, "//button[contains(., 'Accept cookies') or contains(., 'Accept all') or contains(., 'Agree') or contains(., 'Got it') or contains(., 'Close') or contains(., 'Not now') or contains(., 'Continue without') or contains(., 'Dismiss') or contains(@aria-label, 'Dismiss') or contains(@aria-label, 'Close') ]"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, "button[aria-label='Dismiss']"),
            (By.CSS_SELECTOR, "button.artdeco-modal__dismiss"),
            (By.XPATH, "//button[contains(., 'No thanks') or contains(., 'Skip for now') or contains(., 'Maybe later') or contains(., 'Not now')]")
        ]
        for locator in popup_locators:
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                self.safe_click(button)
                time.sleep(1)
                return True
            except Exception:
                continue

        try:
            self.driver.switch_to.alert.dismiss()
            time.sleep(1)
            return True
        except Exception:
            pass

        return False

    def enter_email(self, email="babidash252@gmail.com"):
        self.dismiss_popup()
        email_input = self.find_clickable_with_fallback([
            self.email_or_phone_number_box,
            self.email_or_phone_number_box_alt,
        ])
        self.safe_click(email_input)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password="Babi@252dash"):
        self.dismiss_popup()
        password_input = self.find_clickable_with_fallback([
            self.password_box,
            self.password_box_alt,
        ])
        self.safe_click(password_input)
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
        self.safe_click(submit_btn)
        time.sleep(2)
        self.dismiss_post_login_popup()