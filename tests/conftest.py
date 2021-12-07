import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient

from schema_registry.models import Schema, Version


@pytest.fixture(autouse=True)
def user() -> User:
    return baker.make(User, is_superuser=True, is_active=True)


@pytest.fixture
def api_client(user) -> APIClient:
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture
def schema() -> Schema:
    return baker.make(Schema)


@pytest.fixture
def version(schema: Schema) -> Version:
    return baker.make(Version, schema=schema)
