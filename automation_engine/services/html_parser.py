from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_html_form(html_content, base_url):
    """
    Parses an HTML page and extracts form fields into
    a step-based mapping JSON structure.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    steps = []
    fill_fields = []

    # -------------------------
    # 1️⃣ INPUT & SELECT FIELDS
    # -------------------------
    for element in soup.find_all(["input", "select", "textarea"]):

        element_id = element.get("id")
        element_type = element.name

        if not element_id:
            continue  # selector must exist

        # Ignore buttons
        if element.name == "input" and element.get("type") in ["submit", "button"]:
            continue

        # Determine field type
        field_type = "text"
        if element.name == "select":
            field_type = "select"
        elif element.get("type") == "file":
            field_type = "file"

        fill_fields.append({
            "selector": f"#{element_id}",
            "type": field_type,
            "value": "",          # AI will fill later
            "confidence": 1.0     # placeholder
        })

    if fill_fields:
        steps.append({
            "action": "fill",
            "fields": fill_fields
        })

    # -------------------------
    # 2️⃣ NEXT / BUTTON CLICKS
    # -------------------------
    for button in soup.find_all("button"):
        btn_id = button.get("id")
        if not btn_id:
            continue

        if "next" in btn_id.lower():
            steps.append({
                "action": "click",
                "selector": f"#{btn_id}"
            })

    # -------------------------
    # 3️⃣ SUBMIT BUTTON
    # -------------------------
    submit_button = soup.find("button", {"type": "submit"})
    if submit_button and submit_button.get("id"):
        steps.append({
            "action": "submit",
            "selector": f"#{submit_button.get('id')}"
        })

    return {
        "application_id": None,
        "url": base_url,
        "steps": steps
    }
