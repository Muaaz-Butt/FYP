from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
import threading
from .tasks import run_application

# 1. Your Custom Authentication Class
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Bypass CSRF

@api_view(["POST"])
# 2. Use these specific decorators for function-based views
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def submit_application(request):
    mapping_file = request.data.get("mapping_file")

    if not mapping_file:
        return Response({"error": "No mapping data provided"}, status=400)

    # Start the Selenium/Automation task in a background thread
    threading.Thread(
        target=run_application,
        args=(mapping_file,)
    ).start()

    return Response({
        "status": "processing",
        "message": "Automation has started in the background",
        "mapping_file": mapping_file
    })