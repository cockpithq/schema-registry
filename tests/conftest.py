from typing import Mapping

from django.contrib.auth.models import User
from model_bakery import baker
import pytest
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
def json_schema_data() -> Mapping:
    return {
        'type': 'object',
        'title': 'Test Type',
        'properties': {
            'prop1': {'type': 'integer'},
        },
    }


@pytest.fixture
def schema() -> Schema:
    return baker.make(Schema)


@pytest.fixture
def version(schema: Schema, json_schema_data) -> Version:
    return baker.make(Version, schema=schema, data=json_schema_data)
