from django.conf.urls import url
from .views import main, download

app_name = 'app_tiedostot'
urlpatterns = [
    url(r'tiedostot/$', main, name='tiedostot'),
    url(r'tiedostot/download/(?P<pk>\d+)/$', download, name='download'),
]
