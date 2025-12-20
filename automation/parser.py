from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

def extract_fields(url, chrome_path):
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, "input")
    
    fields = []
    for i in inputs:
        field = {
            "id": i.get_attribute("id"),
            "name": i.get_attribute("name"),
            "placeholder": i.get_attribute("placeholder"),
            "type": i.get_attribute("type")
        }
        fields.append(field)

    driver.quit()
    return fields
