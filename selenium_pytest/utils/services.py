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
from selenium_pytest.utils.Common import get_url

# click login
def signIn(logger):
    driver = get_url()
    logger.info("Driver initialized")

    sign = signInPage(driver)
    logger.info("Sign-in page initialized")
    time.sleep(2)
    sign.enter_email(logger)
    time.sleep(2)
    sign.enter_password(logger)
    time.sleep(2)
    sign.click_submit_button(logger)
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
def logout(driver, logger):
    # Navigate to feed first to ensure the standard navbar (with Me button) is present
    # driver.get("https://www.linkedin.com/feed/")
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Me')]"))
    #     )
    # except Exception:
    #     pass
    # time.sleep(2)

    home = homePage(driver)
    home.click_me_button_xpath()
    logger.info("clicked me button successfully")
    time.sleep(2)
    home.click_sign_out_button()
    logger.info("clicked sign out button successfully")
    return driver


