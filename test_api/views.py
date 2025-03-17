import time
import requests
from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import User, Token
from .serializers import UserInfoSerializer, UserSerializer, TokenSerializer


class SignupView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = Token.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(seconds=settings.TOKEN_LIFETIME),
            )

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": TokenSerializer(token).data["token"],
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get("id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response(
                {"error": "Please provide both id and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = Token.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(seconds=settings.TOKEN_LIFETIME),
        )

        return Response(
            {"token": TokenSerializer(token).data["token"]}, status=status.HTTP_200_OK
        )


class UserInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LatencyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_time = time.time()

        try:
            response = requests.get("https://ya.ru", timeout=10)
            response.raise_for_status()

            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000

            return Response(
                {"latency_ms": round(latency_ms, 2)}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to measure latency: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        all_tokens = request.data.get("all", False)

        if all_tokens:
            Token.objects.filter(user=request.user).delete()
        else:
            auth_token = request.auth
            if auth_token:
                auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
