from typing import Any, Mapping, Optional

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from jsonschema.exceptions import SchemaError
from jsonsubschema import canonicalizeSchema, isSubschema


class Schema(models.Model):
    name = models.SlugField(_('name'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('schema')
        verbose_name_plural = _('schemas')

    def __str__(self):
        return self.name


class VersionQuerySet(models.QuerySet):
    @transaction.atomic
    def create(self, **kwargs):
        schema = kwargs['schema']
        schema = Schema.objects.filter(id=schema.id).select_for_update().get()
        last_version: Optional[Version] = schema.versions.order_by('number').last()
        if last_version:
            last_version.validate_compatibility(kwargs['data'])
            version_number = last_version.number + 1
        else:
            try:
                kwargs['data'] = canonicalizeSchema(kwargs['data'])
            except SchemaError as error:
                raise Version.InvalidSchemaError(error)
            else:
                version_number = 1
        kwargs.setdefault('number', version_number)
        return super().create(**kwargs)


class Version(models.Model):
    class Error(Exception):
        pass

    class NotCompatibleError(Error):
        pass

    class InvalidSchemaError(Error):
        pass

    schema = models.ForeignKey(
        to=Schema,
        on_delete=models.CASCADE,
        related_name='versions',
        related_query_name='version',
        verbose_name=_('schema'),
    )
    number = models.PositiveIntegerField(_('number'), editable=False)
    data = models.JSONField(_('data'), default=dict)
    objects = VersionQuerySet.as_manager()

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')
        unique_together = (
            ('schema', 'number'),
        )

    def __str__(self):
        return '{schema}:{version_number}'.format(schema=self.schema, version_number=self.number)

    def is_compatible(self, data: Mapping[str, Any]) -> bool:
        return isSubschema(data, self.data)

    def validate_compatibility(self, data: Mapping[str, Any]) -> None:
        if not self.is_compatible(data):
            raise self.NotCompatibleError('Schema is not backward compatible.')
