from django.urls import path
from .views import GenerateTokenView, ValidateTokenView, RevokeTokenView, ResourceView

urlpatterns = [
    path("resource/", ResourceView.as_view(), name="get_resource"),
    path("token/generate/", GenerateTokenView.as_view(), name="generate_token"),
    path("token/validate/", ValidateTokenView.as_view(), name="validate_token"),
    path("token/revoke/", RevokeTokenView.as_view(), name="revoke_token"),
]
