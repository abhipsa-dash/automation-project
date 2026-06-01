import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from selenium_pytest.utils.services import signIn, logout
from selenium_pytest.utils.logger import AppLogger
from selenium_pytest.utils.execution_data import record_execution, get_failure_type

logger = AppLogger("signin").get_logger()

if __name__ == "__main__":
    start = time.time()
    try:
        driver = signIn(logger)
        logger.info("Signed in successfully")
        time.sleep(5)
        logout(driver, logger)
        logger.info("Logged out successfully")
        driver.quit()

        record_execution(
            test_name="signin_test",
            status="passed",
            execution_time=time.time() - start,
        )
    except Exception as e:
        elapsed = time.time() - start
        failure_type = get_failure_type(e)
        logger.error(f"signin_test failed: {e}")
        record_execution(
            test_name="signin_test",
            status="failed",
            execution_time=elapsed,
            failure_type=failure_type,
        )
        raise
