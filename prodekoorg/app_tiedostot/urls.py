from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import download, main

app_name = 'app_tiedostot'
urlpatterns = [
    url(_(r'^files/$'), main, name='tiedostot'),
    url(_(r'^files/download/(?P<pk>\d+)/$'), download, name='download'),
]
