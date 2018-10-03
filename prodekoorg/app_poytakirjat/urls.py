from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

app_name = 'app_poytakirjat'
urlpatterns = [
    url(_(r'^documents/'), views.docs, name='documents'),
]
