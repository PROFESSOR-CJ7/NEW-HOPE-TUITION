# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ParentSignupSerializer, ParentLoginSerializer

class SignupView(APIView):
    """
    POST /api/auth/signup/
    """
    def post(self, request):
        serializer = ParentSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Parent registered successfully"},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    """
    POST /api/auth/login/
    Returns JWT access & refresh tokens.
    """
    def post(self, request):
        serializer = ParentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            "access":  str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
