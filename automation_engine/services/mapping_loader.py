import json
from django.conf import settings
from pathlib import Path

def load_mapping(filename):
    path = Path(settings.MEDIA_ROOT) / "mappings" / filename
    with open(path, "r") as f:
        return json.load(f)
