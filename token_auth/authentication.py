from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException

from .models import Token, Resource


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "authentication_failed"


class ResourceUser(AnonymousUser):
    def __init__(self, resource: Resource):
        self.resource = resource

    @property
    def is_authenticated(self):
        return self.resource.is_valid()


class TokenAuthentication(BaseAuthentication):
    """
    Authenticate using a token from the `Authorization` header.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        token_str = (
            auth_header.split("Bearer ")[-1]
            if "Bearer " in auth_header
            else auth_header
        )
        try:
            token = Token.objects.get(token=token_str)
            if token.is_valid():
                return (ResourceUser(token.resource), token)
            raise AuthenticationFailed("Invalid request.")
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")
