from django.urls import path
from .views import apply_to_university

urlpatterns = [
    path('apply-to-university/', apply_to_university, name='apply-to-university'),
]
