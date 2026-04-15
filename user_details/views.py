from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash

# REGISTER
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered"})
        return Response(serializer.errors)


# LOGIN
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response(serializer.errors)


# PROFILE
class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email
        })


# CHANGE PASSWORD
class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old = request.data.get("old_password")
        new = request.data.get("new_password")

        if not user.check_password(old):
            return Response({"error": "Wrong old password"})

        user.set_password(new)
        user.save()

        update_session_auth_hash(request, user)

        return Response({"message": "Password updated"})


# SAMPLE DATA
class SampleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"data": ["sample1", "sample2"]})
