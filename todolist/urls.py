from django.contrib import admin
from django.urls import (
    include,
    path
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from todolist.settings import DOMAIN_SITE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('goals/', include('goals.urls')),
    path('bot/', include('bot.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url=f'http://{DOMAIN_SITE}/api/schema/'), name='swagger-ui'),
]
