import pytest
from rest_framework import status

from schema_registry.models import Schema


@pytest.mark.django_db
def test_create(api_client):
    schema_name = 'MySchema1'
    response = api_client.post('/api/v1/schemas/', data={'name': schema_name})
    assert response.status_code == status.HTTP_201_CREATED
    assert Schema.objects.filter(name=schema_name).exists()


@pytest.mark.django_db
def test_retrieve(api_client, schema):
    response = api_client.get(f'/api/v1/schemas/{schema.name}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == schema.name
