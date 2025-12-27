from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import University, FieldMapping
# from student_data.models import StudentProfile
from .utils import build_application_steps


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from student_data.models import StudentProfile
from student_data.serializers import StudentProfileSerializer
from .services import AIService


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Do nothing, bypassing the check

class GenerateAutomationView(APIView):
    # Order matters: check who they are, then if they are allowed
    authentication_classes = [CsrfExemptSessionAuthentication] 
    permission_classes = [permissions.IsAuthenticated]
   
    def post(self, request):
        target_url = request.data.get("url")
        if not target_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Get data for logged in user
        try:
            # request.user is available because of IsAuthenticated permission
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response({
                "error": "profile_missing",
                "message": "Please complete your application form before using auto-apply."
            }, status=status.HTTP_404_NOT_FOUND)

        student_data = StudentProfileSerializer(profile).data
        
        # 3. Call AI Service
        ai_service = AIService()
        try:
            # Note: Ensure your AIService.get_automation_instructions 
            # accepts target_url, student_data, and app_id
            mapping_result = ai_service.get_automation_instructions(
                target_url=target_url,
                student_data=student_data,
                app_id=profile.id
            )
            
            # Using .dict() because mapping_result is a Pydantic object from LangChain
            return Response(mapping_result.dict(), status=status.HTTP_200_OK)
            
        except Exception as e:
            # Catching AI or Connection errors
            return Response({
                "error": "ai_mapping_failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)