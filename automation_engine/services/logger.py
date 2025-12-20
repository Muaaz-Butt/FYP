from pathlib import Path
from django.conf import settings
import json

def save_screenshot(driver, app_id):
    path = Path(settings.MEDIA_ROOT) / "screenshots"
    path.mkdir(exist_ok=True)
    driver.save_screenshot(str(path / f"{app_id}.png"))

def save_result(app_id, result):
    path = Path(settings.MEDIA_ROOT) / "results"
    path.mkdir(exist_ok=True)

    with open(path / f"{app_id}.json", "w") as f:
        json.dump(result, f, indent=2)
