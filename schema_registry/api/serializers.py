from rest_framework import serializers

from schema_registry.models import Schema, Version


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = 'name', 'versions'
        read_only_fields = ('versions',)


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = 'number', 'data'
        read_only_fields = ('number',)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Version.NotCompatible:
            raise serializers.ValidationError({'data': 'Schema is not backward compatible.'})
