import sentry_sdk
from django.conf import settings


class Catch4xxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.SENTRY_ENABLED and 400 <= response.status_code < 500:  # noqa: WPS432
            sentry_sdk.capture_message('HTTP 4xx error.')
        return response
