"""This Test will go to jobs, click on search, apply necessary filters, show results, Run a loop to print all the jobs returned by the search
Print format:
Title: 
Company:
Location:
Posting datetime:
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from selenium_pytest.utils.services import signIn, logout
from selenium_pytest.pages.homePage import homePage
from selenium_pytest.model.profile_parser import parse_profile
from selenium_pytest.utils.execution_data import record_execution, get_failure_type


def test_get_jobs(driver, logger=None, title=None):
    start = time.time()
    try:
        home_page = homePage(driver)

        home_page.click_search_bar()
        if logger:
            logger.info("Clicked homepage search bar")
        time.sleep(5)

        home_page.enter_search_title(title)
        if logger:
            logger.info(f"Entered title from user.md: {title}")
        time.sleep(5)

        record_execution(
            test_name="get_jobs",
            status="passed",
            execution_time=time.time() - start,
        )
    except Exception as e:
        failure_type = get_failure_type(e)
        record_execution(
            test_name="get_jobs",
            status="failed",
            execution_time=time.time() - start,
            failure_type=failure_type,
        )
        raise


if __name__ == "__main__":
    from selenium_pytest.utils.logger import AppLogger
    logger = AppLogger("get_jobs").get_logger()

    logger.info("Parsing user.md for job title...")
    profile = parse_profile()
    title = profile.get("title", "")
    logger.info(f"Using title from user.md: '{title}'")
    time.sleep(5)

    driver = signIn(logger)
    time.sleep(5)

    try:
        test_get_jobs(driver, logger=logger, title=title)
        time.sleep(5)
    finally:
        time.sleep(5)
        logout(driver, logger)
        driver.quit()
