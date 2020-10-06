from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _
from django.views import defaults as default_views

from config.router import urlpatterns as api_urlpatterns


app_name = 'main_music'


# Admin URLs
admin.site.site_header = _('MUSIC Project')
urlpatterns = [
    path(r'admin/', admin.site.urls),
]

# API URLs
# Create a router and register our resources with it.
urlpatterns += [
    path('api/v1/', include(api_urlpatterns)),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(r'400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path(r'403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path(r'404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path(r'500/', default_views.server_error),
    ]
    # Media URLs on debug
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
