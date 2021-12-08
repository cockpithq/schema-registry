from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


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
        last_version = schema.versions.order_by('number').last()
        version_number = Version.number + 1 if last_version else 1
        kwargs.setdefault('number', version_number)
        return super().create(**kwargs)


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
    objects = VersionQuerySet.as_manager()

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')
        unique_together = (
            ('schema', 'number'),
        )

    def __str__(self):
        return '{schema}:{version_number}'.format(schema=self.schema, version_number=self.number)
