import pytest
from rest_framework import status

from schema_registry.models import Schema


@pytest.mark.django_db
def test_create(api_client, schema: Schema):
    assert not schema.versions.exists()
    response = api_client.post(
        f'/api/v1/schemas/{schema.name}/versions/',
        data={
            'data': {'type': 'number'},
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert schema.versions.filter(number=1).exists()
