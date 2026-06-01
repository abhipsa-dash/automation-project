import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from selenium_pytest.utils.services import signIn, logout
from selenium_pytest.pages.homePage import homePage
from selenium_pytest.utils.execution_data import record_execution, get_failure_type


def test_validate_home_ui(driver, logger):
    start = time.time()
    try:
        home_page = homePage(driver)

        home_page.click_my_network_nav()
        logger.info("Clicked My Network successfully")

        home_page.click_messaging_nav()
        logger.info("Clicked My messaging successfully")

        home_page.click_notifications_nav()
        logger.info("Clicked Notifications successfully")

        home_page.click_home_nav()
        logger.info("Clicked Home successfully")

        record_execution(
            test_name="validate_home_ui",
            status="passed",
            execution_time=time.time() - start,
        )
    except Exception as e:
        failure_type = get_failure_type(e)
        record_execution(
            test_name="validate_home_ui",
            status="failed",
            execution_time=time.time() - start,
            failure_type=failure_type,
        )
        raise


if __name__ == "__main__":
    from selenium_pytest.utils.logger import AppLogger
    logger = AppLogger("validate_home_ui").get_logger()

    driver = signIn(logger)
    time.sleep(5)

    test_validate_home_ui(driver, logger)
    time.sleep(5)

    logout(driver, logger)
    driver.quit()
