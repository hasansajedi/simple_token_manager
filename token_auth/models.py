import hashlib
import uuid
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


class Resource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    identifier = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.valid_until = timezone.now() + timedelta(days=30)
        if not self.identifier:
            self.api_key = hashlib.sha256(self.url.encode()).hexdigest()
            self.identifier = str(uuid.uuid4())

        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.valid_until

    def __str__(self):
        return f"Resource({self.name}, {self.url})"


class Token(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="tokens"
    )
    token = models.CharField(max_length=255, unique=True, db_index=True)
    is_revoked = models.BooleanField(default=False)
    scope = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["is_revoked", "expires_at"]),
        ]
        ordering = ["-created_at"]

    def is_valid(self):
        return not self.is_revoked and now() < self.expires_at

    def revoke(self):
        self.is_revoked = True
        self.save()

    def __str__(self):
        return f"Token({self.token}) @ {self.resource.name}"
