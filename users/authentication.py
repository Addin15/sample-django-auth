from rest_framework import authentication, exceptions
from knox.auth import AuthToken, hash_token

from . import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            t = token.split(" ")
            token = t[2]

        if not token:
            return None

        hashed = hash_token(token=token)

        try:
            payload = AuthToken.objects.filter(
                digest=hashed).first()
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")
        finally:
            if payload == None:
                raise exceptions.AuthenticationFailed("Invalid token")

        user = models.User.objects.filter(id=payload.user.id).first()

        return (user, None)
