from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def robust_click(page, locator, timeout=50):

    wait = WebDriverWait(page.driver, timeout)

    element = wait.until(
        EC.presence_of_element_located(locator)
    )

    page.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    wait.until(
        EC.visibility_of(element)
    )

    wait.until(
        EC.element_to_be_clickable(locator)
    )

    return element

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
        WebDriverWait(driver, 70).until(
            lambda d: any(d.find_elements(*locator) for locator in login_locators)
        )
    except Exception as exc:
        print("Login page did not load the expected form fields.")
        print("Current URL:", driver.current_url)
        print("Exception:", repr(exc))
        traceback.print_exc()
        raise
    return driver