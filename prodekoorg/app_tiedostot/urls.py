from django.urls import re_path
from django.utils.translation import ugettext_lazy as _

from .views import download

app_name = "app_tiedostot"
urlpatterns = [re_path(_(r"^files/download/(?P<pk>\d+)/$"), download, name="download")]
