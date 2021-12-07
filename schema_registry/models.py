from django.db import models
from django.utils.translation import gettext_lazy as _


class Schema(models.Model):
    name = models.SlugField(_('name'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('schema')
        verbose_name_plural = _('schemas')

    def __str__(self):
        return self.name


class Version(models.Model):
    schema = models.ForeignKey(
        to=Schema,
        on_delete=models.CASCADE,
        related_name='versions',
        related_query_name='version',
        verbose_name=_('schema'),
    )
    number = models.PositiveIntegerField(_('number'))
    data = models.JSONField(_('data'), default=dict)

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')
        unique_together = (
            ('schema', 'number'),
        )

    def __str__(self):
        return '{schema}:{version_number}'.format(schema=self.schema, version_number=self.number)
