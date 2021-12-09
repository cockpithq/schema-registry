from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_path = path('api/', include('schema_registry.api.urls'))

urlpatterns = [
    path('admin/', admin.site.urls),
    api_path,
    path('api/schemas/v1/', SpectacularAPIView.as_view(api_version='v1', urlconf=[api_path]), name='schema'),
    path('docs/api/v1/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
