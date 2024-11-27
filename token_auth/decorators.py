from functools import wraps
from django.http import JsonResponse

from .models import Resource


def validate_resource(f):
    """
    To validate resource_id, apikey, and identifier in the request.
    """

    @wraps(f)
    def wrap(view, request, *args, **kwargs):
        if request.method == "POST":
            apikey = request.data.get("apikey")
            identifier = request.data.get("identifier")
        else:
            return JsonResponse(
                {"error": "Missing resource_id, apikey, or identifier."}, status=400
            )

        if not apikey or not identifier:
            return JsonResponse(
                {"error": "Missing resource_id, apikey, or identifier."}, status=400
            )

        try:
            resource = Resource.objects.get(api_key=apikey, identifier=identifier)
        except Resource.DoesNotExist:
            return JsonResponse({"error": "Invalid parameters."}, status=401)

        request.resource = resource
        return f(view, request, *args, **kwargs)

    return wrap
