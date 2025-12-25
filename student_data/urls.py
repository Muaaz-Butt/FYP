
from django.urls import path
from .views import StudentProfileSubmitAPIView

urlpatterns = [

    path('profile/', StudentProfileSubmitAPIView.as_view(), name='student-profile-api'),
]