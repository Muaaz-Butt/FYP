
from django.http import JsonResponse
from .serializers import SignupSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .serializers import SignupSerializer
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from .serializers import SignupSerializer
import json
@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user) 
            return JsonResponse({"message": "Account created successfully"}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    return JsonResponse({"error": "Only POST method allowed"}, status=405)


from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class LoginAPIView(APIView):

    authentication_classes = [] 
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user) 
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Invalid email or password"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_test(request):
    if request.method == "GET":
        return JsonResponse({"message": "CSRF exempt works!"})
    return JsonResponse({"error": "Only GET allowed"}, status=405)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
