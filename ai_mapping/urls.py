from django.urls import path
from .views import generate_automation_steps

urlpatterns = [
    path('map/', generate_automation_steps, name='apply-to-university'),
]
