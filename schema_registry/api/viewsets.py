from functools import cached_property

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from schema_registry.api.serializers import SchemaSerializer, VersionSerializer, VersionValidationSerializer
from schema_registry.models import Schema, Version


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    lookup_field = 'name'


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    lookup_field = 'number'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema=self._schema)

    def perform_create(self, serializer):
        serializer.save(schema=self._schema)

    @action(methods=['post'], detail=False, serializer_class=VersionValidationSerializer)
    def validate(self, request, *args, **kwargs):
        last_version = self._schema.versions.order_by('number').last()
        serializer: VersionValidationSerializer = self.get_serializer(instance=last_version, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @cached_property
    def _schema(self) -> Schema:
        return get_object_or_404(Schema, name=self.kwargs[SchemaViewSet.lookup_field])
