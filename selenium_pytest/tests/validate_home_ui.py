import sys
sys.path.append("C:\\Users\\ABHIP\\Desktop\\automation-project")  # Add the parent directory to the system path

from selenium_pytest.utils.services import signIn
from selenium_pytest.utils.services import logout
from selenium_pytest.pages.homePage import homePage
import time

def test_validate_home_ui(driver):
    home_page = homePage(driver)
    home_page.dismiss_popups()

    # Validate Navbar
    home_page.click_home_nav()
    assert "feed" in home_page.get_current_url()

    home_page.click_my_network_nav()
    assert "mynetwork" in home_page.get_current_url()

    home_page.click_jobs_nav()
    assert "jobs" in home_page.get_current_url()

    home_page.click_messaging_nav()
    assert "messaging" in home_page.get_current_url()

    home_page.click_notifications_nav()
    assert "notifications" in home_page.get_current_url()

    # Validate Me Dropdown
    home_page.click_view_profile()
    assert "in/abhiprava-bhattacharjee-9b1a4b1b8/" in home_page.get_current_url()

    home_page.click_settings()
    assert "settings" in home_page.get_current_url()


if __name__ == "__main__":
    driver = signIn()
    time.sleep(5)
    
    test_validate_home_ui(driver)
    time.sleep(5)  # Keep the browser open for a while before closing
    
    logout(driver)
    driver.quit()  # Close the browser after use