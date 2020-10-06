from django.conf.urls import url, include

from rest_framework import routers

from music_backend.single_view.api.v1.views import WSVViewSet, SingleViewCSVView

router = routers.SimpleRouter()

router.register(r'wsv', viewset=WSVViewSet)

urlpatterns = [
    url(r'^wsv/export-csv/$', SingleViewCSVView.as_view(), name='wsv-export-csv'),
    url(r'^wsv/export-csv/(?P<iswc>\w+)$', SingleViewCSVView.as_view(), name='wsv-export-csv'),
    url(r'^wsv/import-csv/(?P<filename>[^/]+)$', SingleViewCSVView.as_view(), name='wsv-import-csv'),
    url(r'^', include(router.urls)),
]
