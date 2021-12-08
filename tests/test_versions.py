import copy

import pytest
from rest_framework import status

from schema_registry.models import Schema, Version


@pytest.mark.django_db
def test_create_initial_version(api_client, schema: Schema):
    assert not schema.versions.exists()
    response = api_client.post(
        f'/api/v1/schemas/{schema.name}/versions/',
        data={'data': {'type': 'number'}},
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert schema.versions.filter(number=1).exists()


@pytest.mark.django_db
def test_create_new_version(api_client, schema: Schema, version: Version):
    new_json_schema_data = copy.deepcopy(version.data)
    new_json_schema_data['properties']['prop2'] = {'type': 'integer'}
    response = api_client.post(
        f'/api/v1/schemas/{schema.name}/versions/',
        data={'data': new_json_schema_data},
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert schema.versions.filter(number=version.number + 1).exists()


@pytest.mark.django_db
def test_create_new_version_non_compatible(api_client, schema: Schema, version: Version):
    new_json_schema_data = copy.deepcopy(version.data)
    del new_json_schema_data['properties']
    response = api_client.post(
        f'/api/v1/schemas/{schema.name}/versions/',
        data={'data': new_json_schema_data},
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert 'data' in response.data
