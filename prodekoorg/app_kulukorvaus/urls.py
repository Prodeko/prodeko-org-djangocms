from django.conf.urls import url

from .views import download_kulukorvaus_pdf

app_name = 'app_kulukorvaus'
urlpatterns = [
    url(r'download-kulukorvaus/(?P<perustiedot_id>[0-9]+)$',
        download_kulukorvaus_pdf, name='download_kulukorvaus'),
]
