from django.contrib import admin
from .models import Token, Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing resources.
    """

    list_display = ("name", "url", "identifier", "created_at")
    search_fields = ("name", "url", "identifier")
    readonly_fields = ("identifier", "api_key", "created_at")


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tokens.
    """

    list_display = (
        "resource__name",
        "is_revoked",
        "expires_at",
        "created_at",
    )
    list_filter = ("is_revoked", "expires_at", "created_at")
    search_fields = ("resource__name", "token")
    readonly_fields = ("token", "created_at")
