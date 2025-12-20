from selenium import webdriver
from bs4 import BeautifulSoup
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_fields_from_url(university_url):
    """Extracts input, select, and textarea fields from university application page"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(university_url)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    fields = []
    for tag in soup.find_all(['input', 'select', 'textarea']):
        fields.append({
            "tag": tag.name,
            "type": tag.get('type'),
            "name": tag.get('name'),
            "id": tag.get('id'),
            "placeholder": tag.get('placeholder')
        })
    return fields

def map_fields_to_student(fields, student_data):
    """Uses OpenAI to map university form fields to student profile fields"""
    prompt = f"""
    You are given a university application form with fields: {fields}.
    Map each form field to the best matching student data from: {student_data}.
    Return as JSON: portal_field_name -> student_field_name.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        mapping = json.loads(response['choices'][0]['message']['content'])
    except:
        mapping = {}
    return mapping
