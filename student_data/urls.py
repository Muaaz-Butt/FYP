from django.urls import path
from .views import (
    PersonalInfoAPIView,
    AcademicInfoAPIView,
    DocumentUploadAPIView
)

urlpatterns = [
    path('personal-info/', PersonalInfoAPIView.as_view()),
    path('academic-info/', AcademicInfoAPIView.as_view()),
    path('documents/', DocumentUploadAPIView.as_view()),
]