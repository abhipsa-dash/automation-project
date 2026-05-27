"""This will contain all details, functions and xpaths related to user profile"""

from time import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage:
    def __init__(self, driver):
        self.driver = driver

    menu_icon_xpath = "//button[@aria-label='Me']"
    view_profile_xpath = "//a[normalize-space()='View profile']"
    edit_pencil_icon_xpath = "//*[@id='edit-medium'][1]"
    headline_textbox_xpath = "//*[contains(@class, '_0ce8cd65')]"
    industry_textbox_xpath = "//input[@aria-label='Industry*']"
    save_button_xpath = "//button[normalize-space()='Save']"
    add_Section_button_xpath = "//span[text()='Add section'][1]"
    add_about_button_xpath = "//p[text()='Add about']"
    edit_about_button_xpath = "//div[contains(@class,'_9e20bbe4 _50917d1d ecc023c9 _13974296 _946ca9a4 _7a5af70f _38fdb728')]"
    close_about_button_xpath = "//button[contains(@type,'button')][1]"
    add_education_button_xpath = "//p[text()='Add education']"

    def click_menu_icon(self):
        """This will click on the menu icon to open the dropdown menu"""
        self.driver.find_element_by_xpath(self.menu_icon_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", self.view_profile_xpath)))

    def click_view_profile(self):
        """This will click on the profile icon and open the profile page"""
        self.driver.find_element_by_xpath(self.view_profile_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/profile"))

    def click_edit_pencil_icon(self):
        """This will click on the pencil icon to edit the profile details"""
        self.driver.find_element_by_xpath(self.edit_pencil_icon_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", "//input[@name='name']")))

    def update_headline(self, new_headline):
        """This will update the headline of the profile"""
        headline_textbox = self.driver.find_element_by_xpath(self.headline_textbox_xpath)
        headline_textbox.click()
        headline_textbox.clear()
        headline_textbox.send_keys(new_headline)

    def update_industry(self, new_industry):
        """This will update the industry of the profile"""
        industry_textbox = self.driver.find_element_by_xpath(self.industry_textbox_xpath)
        industry_textbox.click()
        industry_textbox.clear()
        industry_textbox.send_keys(new_industry)

    def click_save_button(self):
        """This will click on the save button to save the changes made to the profile"""
        self.driver.find_element_by_xpath(self.save_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", "//span[contains(text(), 'Profile updated')]")))

    def click_add_section_button(self):
        """This will click on the add section button to add a new section to the profile"""
        self.driver.find_element_by_xpath(self.add_Section_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", "//span[text()='Add profile section']")))

    def click_add_about_button(self):
        """This will click on the add about button to add about section to the profile"""
        self.driver.find_element_by_xpath(self.add_about_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", "//span[text()='Add about']")))

    def enter_edit_about_button(self):
        """This will click on the edit about button to edit the about section of the profile"""
        wait = WebDriverWait(self.driver, 10)
        edit_about_button = wait.until(EC.element_to_be_clickable(self.edit_about_button_xpath))
        edit_about_button.click()   
        edit_about_button.clear()
        edit_about_button.send_keys("This is an updated about section for testing purposes.")

    def click_close_about_button(self):
        """This will click on the close about button to close the about section of the profile"""
        self.driver.find_element_by_xpath(self.close_about_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(("xpath", "//span[text()='Add about']")))

    def click_add_education_button(self):
        """This will click on the add education button to add education details to the profile"""
        self.driver.find_element_by_xpath(self.add_education_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(("xpath", "//span[text()='Add education']")))  