from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def robust_click(page, locator, timeout=20):

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