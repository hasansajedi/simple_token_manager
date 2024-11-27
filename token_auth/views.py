from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .decorators import validate_resource
from .models import Token, Resource
from .serializers import TokenSerializer, ResourceSerializer, RevokeTokenSerializer
from .throttles import ScopedSettingThrottle


class GenerateTokenView(APIView):
    """
    Generate a token for the authenticated user and resource.
    """

    throttle_classes = [ScopedSettingThrottle]

    @validate_resource
    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")

        if not identifier:
            return Response(
                {"error": "identifier ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resource = Resource.objects.get(identifier=identifier)
        except Resource.DoesNotExist:
            return Response(
                {"error": "Invalid resource ID."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TokenSerializer(data=request.data, context={"resource": resource})
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(
            TokenSerializer(token).data,
            status=status.HTTP_201_CREATED,
        )


class ValidateTokenView(APIView):
    """
    Validate a token for its validity.
    """

    throttle_classes = [ScopedSettingThrottle]

    def post(self, request):
        token_str = request.data.get("token")

        if not token_str:
            return Response(
                {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = Token.objects.get(token=token_str)
            if token.is_valid():
                return Response(
                    {"valid": True},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"valid": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Token.DoesNotExist:
            return Response(
                {"valid": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RevokeTokenView(APIView):
    """
    Revoke a token associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = RevokeTokenSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            token = serializer.validated_data["token"]
            token.revoke()
            return Response(
                {"message": "Token revoked successfully."}, status=status.HTTP_200_OK
            )

        return Response({"error": "Invalid token."}, status=status.HTTP_404_NOT_FOUND)


class ResourceView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
