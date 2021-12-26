import logging

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class DefaultAppConfig(AppConfig):
    name = 'schema_registry'
    verbose_name = _('Schema Registry')

    def ready(self) -> None:
        if settings.SENTRY_ENABLED:
            from schema_registry.sentry import init  # noqa: F401,WPS433
        else:
            logger.warning('Sentry is disabled, set SENTRY_DSN to enable it.')
