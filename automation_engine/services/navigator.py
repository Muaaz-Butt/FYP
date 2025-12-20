from selenium.webdriver.common.by import By
import time

def click_element(driver, selector):
    driver.find_element(By.CSS_SELECTOR, selector).click()
    time.sleep(1)
