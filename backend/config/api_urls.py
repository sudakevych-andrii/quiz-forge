"""Routes under /api/v1/. Each app adds its own include() here."""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from common.views import HealthView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    # OpenAPI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
