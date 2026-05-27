"""This will login, go to the homepage, go to profile, and validate all the user personal details"""

import sys
# sys.path.append("C:\\Users\\ABHIP\\Desktop\\automation-project")
sys.path.append("D:\\Abby\\automation-project")  # Add the parent directory to the system path

from selenium_pytest.tests.validate_home_ui import test_validate_home_ui
from selenium_pytest.utils.services import signIn
from selenium_pytest.utils.services import logout
from selenium_pytest.pages.profilePage import ProfilePage
import time

def test_validate_profile_info(driver):
    profile_page = ProfilePage(driver)

    # Click on the menu icon to open the dropdown menu  
    profile_page.click_menu_icon()
    profile_page.click_view_profile()
    profile_page.click_edit_pencil_icon()
    profile_page.update_headline("Software Engineer at XYZ Company")    
    profile_page.update_industry("Information Technology and Services")         
    profile_page.click_save_button()
    time.sleep(2)  # Wait for the changes to be saved

if __name__ == "__main__":
    driver = signIn()
    time.sleep(5)
    
    test_validate_profile_info(driver)
    time.sleep(5)  # Keep the browser open for a while before closing
    
    logout(driver)
    driver.quit()  # Close the browser after use