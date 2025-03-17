from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Token


class BearerTokenAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = "Invalid token header. No credentials provided."
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid token header. Token string should not contain spaces."
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "Invalid token header. Token string should not contain invalid characters."
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request):
        try:
            token = Token.objects.select_related("user").get(key=key)
        except (Token.DoesNotExist, ValueError):
            raise AuthenticationFailed("Invalid token.")

        if token.expires_at < timezone.now():
            token.delete()
            raise AuthenticationFailed("Token has expired.")

        if not request.path.endswith("/signin/"):
            token.expires_at = timezone.now() + timedelta(
                seconds=settings.TOKEN_LIFETIME
            )
            token.save()

        return (token.user, token)
