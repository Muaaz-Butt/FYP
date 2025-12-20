from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import StudentProfile
from .serializers import PersonalInfoSerializer, AcademicInfoSerializer,DocumentUploadSerializer


class PersonalInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            return Response({"error": "Profile already exists"}, status=400)
        except StudentProfile.DoesNotExist:
            pass

        serializer = PersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Personal info saved"}, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "No profile found"}, status=404)

        serializer = PersonalInfoSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Personal info updated"}, status=200)
        return Response(serializer.errors, status=400)
class AcademicInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Profile not found - complete personal info first"}, status=404)

        serializer = AcademicInfoSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Academic info saved"}, status=200)
        return Response(serializer.errors, status=400)
from rest_framework.parsers import MultiPartParser, FormParser

class DocumentUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  

    def put(self, request):
        profile = StudentProfile.objects.get(user=request.user)

        serializer = DocumentUploadSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Documents uploaded successfully"})

        return Response(serializer.errors, status=400)
