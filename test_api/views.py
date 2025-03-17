from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import User, Token
from .serializers import UserSerializer, TokenSerializer


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
