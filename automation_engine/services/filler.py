from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

CONFIDENCE_THRESHOLD = 0.85

def fill_fields(driver, fields, errors):
    for field in fields:
        try:
            if field.get("confidence", 1) < CONFIDENCE_THRESHOLD:
                errors.append({
                    "field": field["selector"],
                    "error": "Low confidence"
                })
                continue

            element = driver.find_element(By.CSS_SELECTOR, field["selector"])

            if field["type"] == "text":
                element.clear()
                element.send_keys(field["value"])

            elif field["type"] == "select":
                Select(element).select_by_visible_text(field["value"])

            time.sleep(0.3)

        except Exception as e:
            errors.append({
                "field": field["selector"],
                "error": str(e)
            })
