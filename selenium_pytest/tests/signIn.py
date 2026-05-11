import sys
sys.path.append("C:\\Users\\ABHIP\\Desktop\\automation-project")  # Add the parent directory to the system path

from selenium_pytest.pages.signInPage import signInPage
from selenium_pytest.utils.services import get_url
import time

def test_signIn():
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

if __name__ == "__main__":
    driver = test_signIn()
    time.sleep(5)  # Keep the browser open for a while before closing
    driver.quit()  # Close the browser after use
