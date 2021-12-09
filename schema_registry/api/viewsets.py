from functools import cached_property

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from schema_registry.api.serializers import SchemaSerializer, VersionSerializer
from schema_registry.models import Schema, Version


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    lookup_field = 'name'


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    lookup_field = 'number'

    @cached_property
    def _schema(self) -> Schema:
        return get_object_or_404(Schema, name=self.kwargs[SchemaViewSet.lookup_field])

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema=self._schema)

    def perform_create(self, serializer):
        serializer.save(schema=self._schema)
