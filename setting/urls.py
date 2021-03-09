"""mangame URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # api
    path('api/', include('core.api.urls')),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view( template_name="swagger-ui.html", url_name="schema"), name="swagger-ui")
]