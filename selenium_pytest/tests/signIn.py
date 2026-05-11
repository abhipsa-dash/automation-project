import sys
sys.path.append("C:\\Users\\ABHIP\\Desktop\\automation-project")  # Add the parent directory to the system path

from selenium_pytest.utils.services import signIn
import time


if __name__ == "__main__":
    driver = signIn()
    time.sleep(5)  # Keep the browser open for a while before closing
    driver.quit()  # Close the browser after use
