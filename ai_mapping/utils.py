# from selenium import webdriver
# from bs4 import BeautifulSoup
# import openai
# import os
# import json

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def extract_fields_from_url(university_url):
#     """Extracts input, select, and textarea fields from university application page"""
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)
#     driver.get(university_url)

#     html = driver.page_source
#     driver.quit()

#     soup = BeautifulSoup(html, 'html.parser')
#     fields = []
#     for tag in soup.find_all(['input', 'select', 'textarea']):
#         fields.append({
#             "tag": tag.name,
#             "type": tag.get('type'),
#             "name": tag.get('name'),
#             "id": tag.get('id'),
#             "placeholder": tag.get('placeholder')
#         })
#     return fields

# def map_fields_to_student(fields, student_data):
#     """Uses OpenAI to map university form fields to student profile fields"""
#     prompt = f"""
#     You are given a university application form with fields: {fields}.
#     Map each form field to the best matching student data from: {student_data}.
#     Return as JSON: portal_field_name -> student_field_name.
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     try:
#         mapping = json.loads(response['choices'][0]['message']['content'])
#     except:
#         mapping = {}
#     return mapping

import requests
from bs4 import BeautifulSoup

def parse_application_form(url):
    """
    Fetches and parses an HTML form and extracts all input fields.
    """
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    fields = []

    for field in soup.find_all(["input", "select", "textarea"]):
        field_type = field.get("type", "text")
        field_id = field.get("id")
        field_name = field.get("name")

        # Try to find label text
        label_text = None
        if field_id:
            label = soup.find("label", attrs={"for": field_id})
            if label:
                label_text = label.text.strip()

        # Extract select options
        options = []
        if field.name == "select":
            for option in field.find_all("option"):
                options.append(option.text.strip())

        fields.append({
            "tag": field.name,
            "type": field_type,
            "id": field_id,
            "name": field_name,
            "label": label_text,
            "options": options
        })

    return fields

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def match_fields_with_gemini(parsed_fields, student_data):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key="AIzaSyA3pgSxMyriH2MPRtHbwuaOSG8bN_Cbmek",
        temperature=0
    )

    system_prompt = """
You are an AI that maps HTML form fields to student profile data.

Return STRICT JSON in the following format:

{
  "steps": [
    {
      "action": "fill",
      "fields": [
        {
          "selector": "#field_id",
          "type": "text | select | radio | checkbox | file",
          "value": "student_value",
          "confidence": 0.0-1.0
        }
      ]
    },
    {
      "action": "submit",
      "selector": "#submitBtn"
    }
  ]
}

Rules:
- Use CSS selectors (#id preferred)
- Confidence must be realistic
- Skip fields if no match found
- Do NOT add explanations
"""

    user_prompt = f"""
HTML FORM FIELDS:
{json.dumps(parsed_fields, indent=2)}

STUDENT PROFILE DATA:
{json.dumps(student_data, indent=2)}
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    return json.loads(response.content)

def serialize_student(student):
    return {
        # =====================
        # PERSONAL INFORMATION
        # =====================
        "student_name": student.student_name,
        "student_cnic": student.student_cnic,
        "dob": str(student.dob) if student.dob else None,
        "gender": student.gender,
        "mobile": student.mobile,
        "email": student.email,
        "nationality": student.nationality,
        "religion": student.religion,
        "province": student.province,
        "city": student.city,
        "address": student.address,
        "domicile": student.domicile,
        "hafiz_quran": student.hafiz_quran,
        "hostel": student.hostel,

        # =====================
        # FATHER / GUARDIAN
        # =====================
        "father_name": student.father_name,
        "father_cnic": student.father_cnic,
        "father_phone": student.father_phone,
        "father_income": student.father_income,

        "mother_name": student.mother_name,

        "guardian_name": student.guardian_name,
        "guardian_mobile": student.guardian_mobile,
        "guardian_cnic": student.guardian_cnic,

        # =====================
        # ACADEMIC INFORMATION
        # =====================
        "matric_obtained": student.matric_obtained,
        "matric_total": student.matric_total,
        "matric_roll": student.matric_roll,
        "board": student.board,

        "inter_part_one": student.inter_part_one,
        "inter_total": student.inter_total,
        "inter_roll": student.inter_roll,

        "preference1": student.preference1,
        "preference2": student.preference2,
        "preference3": student.preference3,

        # =====================
        # DOCUMENT UPLOADS
        # =====================
        "photo": student.photo.url if student.photo else None,
        "matric_degree": student.matric_degree.url if student.matric_degree else None,
        "inter_degree": student.inter_degree.url if student.inter_degree else None,
        "domicile_upload": student.domicile_upload.url if student.domicile_upload else None,
    }
def serialize_student(student):
    return {
        # =====================
        # PERSONAL INFORMATION
        # =====================
        "student_name": student.student_name,
        "student_cnic": student.student_cnic,
        "dob": str(student.dob) if student.dob else None,
        "gender": student.gender,
        "mobile": student.mobile,
        "email": student.email,
        "nationality": student.nationality,
        "religion": student.religion,
        "province": student.province,
        "city": student.city,
        "address": student.address,
        "domicile": student.domicile,
        "hafiz_quran": student.hafiz_quran,
        "hostel": student.hostel,

        # =====================
        # FATHER / GUARDIAN
        # =====================
        "father_name": student.father_name,
        "father_cnic": student.father_cnic,
        "father_phone": student.father_phone,
        "father_income": student.father_income,

        "mother_name": student.mother_name,

        "guardian_name": student.guardian_name,
        "guardian_mobile": student.guardian_mobile,
        "guardian_cnic": student.guardian_cnic,

        # =====================
        # ACADEMIC INFORMATION
        # =====================
        "matric_obtained": student.matric_obtained,
        "matric_total": student.matric_total,
        "matric_roll": student.matric_roll,
        "board": student.board,

        "inter_part_one": student.inter_part_one,
        "inter_total": student.inter_total,
        "inter_roll": student.inter_roll,

        "preference1": student.preference1,
        "preference2": student.preference2,
        "preference3": student.preference3,

        # =====================
        # DOCUMENT UPLOADS
        # =====================
        "photo": student.photo.url if student.photo else None,
        "matric_degree": student.matric_degree.url if student.matric_degree else None,
        "inter_degree": student.inter_degree.url if student.inter_degree else None,
        "domicile_upload": student.domicile_upload.url if student.domicile_upload else None,
    }


def build_application_steps(application_id, url, student):
    parsed_fields = parse_application_form(url)
    student_data = serialize_student(student)

    steps = match_fields_with_gemini(parsed_fields, student_data)

    return {
        "application_id": application_id,
        "url": url,
        "steps": steps["steps"]
    }