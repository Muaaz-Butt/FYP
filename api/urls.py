from django.urls import path
from .views import parse_form, map_fields, submit_application

urlpatterns = [
    path("parse/", parse_form),
    path("map/", map_fields),
    path("submit/", submit_application),
]
