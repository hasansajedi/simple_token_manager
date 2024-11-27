import factory
from datetime import timedelta
from django.utils.timezone import now
from token_auth.models import Resource, Token


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    name = factory.Sequence(lambda n: f"Resource {n}")
    url = factory.Sequence(lambda n: f"https://example{n}.com")
    api_key = factory.Faker("sha256")
    identifier = factory.Faker("uuid4")
    valid_until = now() + timedelta(days=30)


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    resource = factory.SubFactory(ResourceFactory)
    token = factory.Faker("sha256")
    is_revoked = False
    expires_at = now() + timedelta(days=30)
