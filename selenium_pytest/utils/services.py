import time 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time as thread

def get_url():
    #set up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
    
    #navigate to the URL
    driver.get("https://www.linkedin.com")
    driver.maximize_window()
    thread.sleep(5)  # Wait for the page to load
    return driver