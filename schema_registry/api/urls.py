from django.urls import include, path
from rest_framework import routers

from schema_registry.api.viewsets import SchemaViewSet, VersionViewSet

router = routers.DefaultRouter()
router.register('(?P<version>(v1))/schemas', SchemaViewSet)
router.register(r'(?P<version>(v1))/schemas/(?P<name>[\w-]+)/versions', VersionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
