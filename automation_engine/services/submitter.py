from selenium.webdriver.common.by import By
import time

def submit_form(driver, selector):
    driver.find_element(By.CSS_SELECTOR, selector).click()
    time.sleep(3)
