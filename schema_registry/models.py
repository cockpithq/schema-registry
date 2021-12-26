from typing import Any, Mapping, Optional

from django.core.exceptions import ValidationError
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

    def clean(self) -> None:
        try:
            self._pre_save(False)
        except Version.Error as error:
            raise ValidationError({'data': str(error)})

    @transaction.atomic
    def save(self, *args, **kwargs) -> None:
        self._pre_save()
        super().save(*args, **kwargs)

    def _pre_save(self, with_lock=True):
        try:
            self.data = canonicalizeSchema(self.data)
        except SchemaError as error:
            raise Version.InvalidSchemaError(error)
        if not self.pk:
            schema_queryset = Schema.objects.filter(id=self.schema_id)
            if with_lock:
                schema_queryset = schema_queryset.select_for_update()
            schema = schema_queryset.get()
            last_version: Optional[Version] = schema.versions.order_by('number').last()
            if last_version:
                last_version.validate_compatibility(self.data)
                self.number = last_version.number + 1
            else:
                self.number = 1
