from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from automation.parser import extract_fields
from automation.mapper_llm import map_fields_llm
from automation.filler import fill_form

CHROME_PATH = "C:/Users/HP/Downloads/chromedriver-win64/chromedriver.exe"

STUDENT_DATA = {
    "student_name": "Ali Khan",
    "student_cnic": "12345-1111111-1",
    "father_name": "Ahmed Khan"
}

@api_view(["POST"])
def parse_form(request):
    url = request.data.get("url")
    fields = extract_fields(url, CHROME_PATH)
    return Response({"fields": fields})

@api_view(["POST"])
def map_fields(request):
    fields = request.data.get("fields")
    mappings = map_fields_llm(fields)
    return Response({"mappings": mappings})

@api_view(["POST"])
def submit_application(request):
    url = request.data.get("url")
    mappings = request.data.get("mappings")

    result = fill_form(url, mappings, STUDENT_DATA, CHROME_PATH)
    return Response(result)
