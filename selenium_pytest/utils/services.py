import time 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
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
    thread.sleep(5)  # Wait for the page to load
    return driver

def signIn():
    driver = get_url()

    sign = signInPage(driver)
    time.sleep(2)
    sign.enter_email()
    time.sleep(2)
    sign.enter_password()
    time.sleep(2)
    sign.click_submit_button()
    time.sleep(2)  # Keep the browser open for a while before closing
    return driver

def logout(driver):
    home = homePage(driver)
    home.click_profile_icon()
    time.sleep(2)
    home.click_sign_out_button()
    return driver