import json
import os
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

EXECUTION_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "selpy_app", "system", "execution_data"
)
EXECUTION_HISTORY_FILE = os.path.join(EXECUTION_DATA_DIR, "execution_history.json")


def get_failure_type(exception: Exception) -> str:
    if isinstance(exception, (NoSuchElementException, TimeoutException, ElementNotInteractableException)):
        return "locator_failure"
    if isinstance(exception, AssertionError):
        return "assertion_failure"
    return "general_failure"


def record_execution(test_name: str, status: str, execution_time: float, failure_type: str = None) -> dict:
    os.makedirs(EXECUTION_DATA_DIR, exist_ok=True)

    record = {
        "test_name": test_name,
        "framework": "selenium",
        "execution_time": round(execution_time, 2),
        "status": status,
        "failure_type": failure_type,
        "timestamp": datetime.now().isoformat(),
    }

    history = []
    if os.path.exists(EXECUTION_HISTORY_FILE):
        with open(EXECUTION_HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(record)

    with open(EXECUTION_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return record
