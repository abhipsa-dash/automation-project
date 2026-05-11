import time 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time as thread

def get_url():
    # set up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # navigate directly to LinkedIn login
    driver.get("https://www.linkedin.com/login")
    driver.maximize_window()
    thread.sleep(5)  # Wait for the page to load
    return driver