from rest_framework import serializers

from schema_registry.models import Schema, Version


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = 'name', 'versions'
        read_only_fields = ('versions',)


class VersionValidationSerializer(serializers.Serializer):
    data = serializers.JSONField()  # type: ignore

    def validate_data(self, value):
        try:
            return self.instance.validate_compatibility(value)
        except Version.Error as error:
            raise serializers.ValidationError(str(error))


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = 'number', 'data'
        read_only_fields = ('number',)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Version.Error as error:
            raise serializers.ValidationError({'data': str(error)})
