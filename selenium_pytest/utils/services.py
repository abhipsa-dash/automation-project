import time 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium_pytest.pages.signInPage import signInPage
from selenium_pytest.pages.homePage import homePage
import time as thread

def get_url():
    # set up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # navigate directly to LinkedIn login
    driver.get("https://www.linkedin.com/login")
    driver.maximize_window()
    login_locators = [
        (By.CSS_SELECTOR, "input[name='session_key']"),
        (By.CSS_SELECTOR, "input#username"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ]
    try:
        WebDriverWait(driver, 20).until(
            lambda d: any(d.find_elements(*locator) for locator in login_locators)
        )
    except Exception as exc:
        print("Login page did not load the expected form fields.")
        print("Current URL:", driver.current_url)
        raise
    return driver

# click login
def signIn():
    driver = get_url()

    sign = signInPage(driver)
    time.sleep(2)
    sign.enter_email()
    time.sleep(2)
    sign.enter_password()
    time.sleep(2)
    sign.click_submit_button()
    time.sleep(3)
    
    # Wait for home page to load
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/feed/')]"))
        )
    except Exception:
        pass
    
    time.sleep(2)
    return driver

#click logout
def logout(driver):
    home = homePage(driver)
    home.click_profile_icon()
    time.sleep(2)
    home.click_sign_out_button()
    return driver