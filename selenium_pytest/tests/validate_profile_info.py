"""This will login, go to the homepage, go to profile, and validate all the user personal details"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from selenium_pytest.utils.services import signIn, logout
from selenium_pytest.pages.profilePage import ProfilePage
from selenium_pytest.utils.execution_data import record_execution, get_failure_type


def test_validate_profile_info(driver):
    start = time.time()
    try:
        profile_page = ProfilePage(driver)

        profile_page.click_menu_icon()
        profile_page.click_view_profile()
        profile_page.click_edit_pencil_icon()
        profile_page.update_headline("Software Engineer at XYZ Company")
        profile_page.update_industry("Information Technology and Services")
        profile_page.click_save_button()
        time.sleep(2)

        record_execution(
            test_name="validate_profile_info",
            status="passed",
            execution_time=time.time() - start,
        )
    except Exception as e:
        failure_type = get_failure_type(e)
        record_execution(
            test_name="validate_profile_info",
            status="failed",
            execution_time=time.time() - start,
            failure_type=failure_type,
        )
        raise


if __name__ == "__main__":
    from selenium_pytest.utils.logger import AppLogger
    logger = AppLogger("validate_profile_info").get_logger()

    driver = signIn(logger)
    time.sleep(5)

    test_validate_profile_info(driver)
    time.sleep(5)

    logout(driver, logger)
    driver.quit()
