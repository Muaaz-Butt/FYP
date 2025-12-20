from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def fill_form(url, mappings, student_data, chrome_path):
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(1)

    for m in mappings:
        field_id = m.get("id")
        mapped_key = m.get("mapped_to")

        if mapped_key is None:
            continue
        
        value = student_data.get(mapped_key)
        if value is None:
            continue
        
        try:
            input_box = driver.find_element(By.ID, field_id)
            input_box.send_keys(str(value))
        except:
            pass

    # press submit if button exists
    try:
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()
    except:
        pass

    time.sleep(2)
    driver.quit()

    return {"status": "submitted"}
