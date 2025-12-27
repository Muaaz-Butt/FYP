from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import GenerateAutomationView

urlpatterns = [
    # Wrapping the view in csrf_exempt bypasses the token check
    path('generate-mapping/', csrf_exempt(GenerateAutomationView.as_view()), name='generate-mapping'),
]