from asyncio import wait
import email
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_pytest.utils.Common import robust_click, get_url

class signInPage:
    def __init__(self, driver):
        self.driver = driver
        # LinkedIn frequently toggles between these sets of IDs
        self.email_or_phone_number_box = (By.XPATH, "//input[starts-with(@id, ':r3')]") 
        self.email_or_phone_number_box_alt = (By.XPATH, "//input[starts-with(@id, ':r6')]")
    
        self.password_box = (By.XPATH, "//input[starts-with(@id, ':r7')]")
        self.password_box_alt = (By.XPATH, "//input[starts-with(@id, ':r4')]")
    
        self.submit_button = (By.XPATH, "//span[text()='Forgot password?'][1]/following::button[@type='button'][5]")
        # self.submit_button_alt = (By.XPATH, "//span[text()='Sign in'][1]")
    
 
    def enter_email(self, email="babidash252@gmail.com"):

        try:
            print("inside enter_email, trying primary locator")
            email_input = robust_click(
            self,
            self.email_or_phone_number_box
        )
        except Exception as e:
            print(f"enter_email: failed to click primary locator: {e}")
            # try alternative locator
            try:
                print("Trying alternative locator for email input")
                get_url().refresh()  # Refresh the page to reset any potential issues
                email_input = robust_click(
                    self,
                    self.email_or_phone_number_box_alt
                )
            except Exception as e2:
                print(f"enter_email: failed to click alternative locator: {e2}")
                raise

        email_input.clear()

        time.sleep(1)

        email_input.send_keys(email)
        print("Email entered successfully")
       
 
    def enter_password(self, password="Babi@252dash"):
        wait = WebDriverWait(self.driver, 10)
        try:
            print("inside enter_password, trying primary locator")
            password_input = wait.until(EC.element_to_be_clickable(self.password_box))
        except:    
            print("Trying alternative locator for password input")        
            password_input = wait.until(EC.element_to_be_clickable(self.password_box_alt))
            
        password_input.click()
        password_input.clear()
        password_input.send_keys(password)
        print("Password entered successfully")

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
        # wait = WebDriverWait(self.driver, 10)
        # try:
        #     print("inside click_submit_button, trying primary locator")
        #     submit_btn = wait.until(EC.element_to_be_clickable(self.submit_button))
        # except:    
        #     print("Trying alternative locator for click_submit_button")        
        #     submit_btn = wait.until(EC.element_to_be_clickable(self.submit_button_alt))
        wait = WebDriverWait(self.driver,10)
        print("inside click_submit_button")
        submit_btn = wait.until(EC.element_to_be_clickable(self.submit_button))
        submit_btn.click()
        print("successfully signed in")
        time.sleep(2)
        self.dismiss_post_login_popup()