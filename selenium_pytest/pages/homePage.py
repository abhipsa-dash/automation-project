import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_pytest.utils.Common import robust_click
from selenium.webdriver.common.by import By

"""This will contain all details, functions and xpaths related to the homepage"""

class homePage:
    def __init__(self, driver):
        self.driver = driver

    def dismiss_popups(self):
        # Remove dialogs/overlays that can intercept navigation clicks
        self.driver.execute_script(
            "document.querySelectorAll('dialog, div[role=dialog], div[role=alert], div[class*=overlay], div[class*=modal], section[class*=cookie]').forEach(el => el.remove());"
        )
        time.sleep(1)

    # click Logout xpaths
    profile_icon_xpath = "//button[@data-view-name='navigation-settings']"
    sign_out_button_xpath = "//a[normalize-space()='Sign out']" 

    search_bar_xpath = "//input[contains(@placeholder,'Search')]"  #search_bar_xpath   

    # Feed xpaths 
    feed_post_xpath = "//div[contains(@class,'feed-shared-update-v2')]"
    start_a_post_xpath = "//button[contains(@class,'share-box-feed-entry__trigger')]"

    # Post modal xpaths 
    post_text_box_xpath = "//div[@role='textbox']"
    post_submit_button_xpath = "//button[contains(@class,'share-actions__primary-action')]"

    # Like xpaths 
    like_button_xpath = "(//button[contains(@aria-label,'React Like')])[1]"

    # Comment xpaths 
    comment_button_xpath = "(//button[contains(@aria-label,'Comment')])[1]"
    comment_textbox_xpath = "//div[@role='textbox' and contains(@class,'comments-comment-box')]"
    comment_submit_xpath = "//button[contains(@class,'comments-comment-box__submit-button')]"

    # Navbar xpaths
    home_nav_xpath = "//span[text()='Home']/ancestor::a"
    my_network_nav_xpath = "//span[text()='My Network']/ancestor::a"
    jobs_nav_xpath = "//span[text()='Jobs']/ancestor::a"
    messaging_nav_xpath = "//span[text()='Messaging']/ancestor::a"
    notifications_nav_xpath = "//span[text()='Notifications']/ancestor::a"

    # Me dropdown xpaths 
    me_button_xpath = "//button[contains(@class,'global-nav__primary-link') and .//span[text()='Me']]"
    view_profile_xpath = "//a[contains(@href,'/in/') and contains(.,'View Profile')]"
    settings_xpath = "//a[contains(@href,'/settings/')]"

    def close_message_overlay(self):

        try:

            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@aria-label,'Close your conversation')]"
                    )
                )
            )

            close_btn.click()

            time.sleep(2)

        except Exception:
            pass
 
 
    # Search methods 

    def search_keyword(self, keyword):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.search_bar_xpath))
        ).click()
        robust_click(self, self.search_bar_xpath)
        self.driver.find_element("xpath", self.search_bar_xpath).send_keys("QE Engineer")
        self.driver.find_element("xpath", self.search_bar_xpath).send_keys(Keys.RETURN)
        time.sleep(2)

    def get_search_suggestions(self, keyword):
        self.driver.find_element("xpath", self.search_bar_xpath).send_keys("QE Engineer")
        time.sleep(1)
        return self.driver.find_elements("xpath", "//div[contains(@class,'search-typeahead-v2__hit')]")

     # Feed methods

    def is_feed_loaded(self):
        posts = self.driver.find_elements("xpath", self.feed_post_xpath)
        return len(posts) > 0

    def scroll_feed(self, times=3):
        for _ in range(times):
            self.driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1)

 
    # Create Post methods

    def click_start_a_post(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.start_a_post_xpath))
        ).click()
        time.sleep(1)

    def create_post(self, text):
        self.click_start_a_post()
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(("xpath", self.post_text_box_xpath))
        ).send_keys("This is an automated post created by Selenium.")
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.post_submit_button_xpath))
        ).click()
        time.sleep(3)

 
    # Like / Unlike methods

    def like_first_post(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.like_button_xpath))
        ).click()
        time.sleep(1)

    def unlike_first_post(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.like_button_xpath))
        ).click()
        time.sleep(1)

    def is_post_liked(self):
        like_btn = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(("xpath", self.like_button_xpath))
        )
        return like_btn.get_attribute("aria-pressed") == "true"

    # Comment methods

    def comment_on_first_post(self, comment_text):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.comment_button_xpath))
        ).click()
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(("xpath", self.comment_textbox_xpath))
        ).send_keys("This is an automated comment created by Selenium.")
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(("xpath", self.comment_submit_xpath))
        ).click()
        time.sleep(2)

    # Navbar methods

    def click_my_network_nav(self):
        self.dismiss_popups()
        robust_click(self, ("xpath", self.my_network_nav_xpath)).click()
        time.sleep(5)

    def click_jobs_nav(self):
        self.dismiss_popups()
        robust_click(self, ("xpath", self.jobs_nav_xpath)).click()
        time.sleep(5)

    def click_messaging_nav(self):
        self.dismiss_popups()
        robust_click(
        self,
        (By.XPATH, self.messaging_nav_xpath)).click()
        time.sleep(5)
        self.close_message_overlay()

    def click_notifications_nav(self):
        self.dismiss_popups()
        notification_btn = robust_click(
        self,
        (By.XPATH, self.notifications_nav_xpath))
        self.driver.execute_script(
        "arguments[0].click();",
        notification_btn
        )
        time.sleep(5)

    def get_current_url(self):
        return self.driver.current_url

    # Me Dropdown methods

    def click_me_button(self):
        robust_click(self, ("xpath", self.me_button_xpath)).click()
        time.sleep(1)

    def click_view_profile(self):
        self.click_me_button()
        robust_click(self, ("xpath", self.view_profile_xpath)).click()
        time.sleep(2)

    def click_settings(self):
        self.click_me_button()
        robust_click(self, ("xpath", self.settings_xpath)).click()
        time.sleep(2)

#logout functions
    def click_profile_icon(self):
        robust_click(self, ("xpath", self.profile_icon_xpath)).click()

    def click_sign_out_button(self):
        self.robust_click(self.sign_out_button_xpath)